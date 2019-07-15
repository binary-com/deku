import docker
import logging
import json
import re
from time import sleep

class Image:
    def __init__(self, image):
        match = re.match('(.*):(.*)@(sha256:.*)', image)
        if match:
            [name, tag, digest] = match.groups()
            self.name = name
            self.tag = tag
            self.digest = digest

class Services:
    def __init__(self, client):
        self.client = client

    def is_docker_running(self):
        """
        Check if Docker client is running.
        """
        try:
            return self.client.ping();
        except docker.errors.APIError as e:
            logging.warn('Docker service is down: %s' % (e))
        except:
            logging.warn('Docker service is down: Unexpected error occured')

        return False



    def get(self, filters=None):
        """
        Get Docker services based on the filter provided, if no filter is passed then all the running services are returned
        """
        if self.is_docker_running():
            return self.client.services.list(filters=filters)
        return []

    def update(self, **kwargs):
        """
        Update docker services 

        Arguments:
            
            "filters": Filter services based on id, name, mode or label. Passed as dictionary.

            "update_config": Dictionary of service options updates
        """
        service_list = []
        response = {}

        if 'filters' in kwargs:
            service_list = self.get(filters=kwargs['filters'])
        else:
            # Get all the services
            service_list = self.get()

        if len(service_list):
            logging.info('Updating services...')
        else:
            logging.info('No services to update')
            logging.info(json.dumps(kwargs))
            response['Error'] = 'No services to update'

        completed_services = 0
        for service in service_list:
            response[service.name] = {}
            try:
                service.update(**kwargs['update_config'])
                response[service.name]['Status'] = "updating"
                response[service.name]['Message'] = "Update has been initaited"

            except docker.errors.APIError as e:
                completed_services += 1
                logging.warn('Update failed for service %s : %s' %(service.name, e))
                response[service.name]['Message'] = 'Update failed with error "%s"' %(e)
                response[service.name]['Status'] = 'failed'

        return response

    def get_status(self, filters=None):
        """
        Get last status of service updates
        """
        service_list = self.get(filters=filters)
        response = {}
        for service in service_list:
            response[service.name] = {}
            updateStatus = service.attrs.get('UpdateStatus')
            if updateStatus:
                if 'Message' in updateStatus: response[service.name]['Message'] = updateStatus['Message']
                if 'Image' in updateStatus: response[service.name]['Image'] = service.attrs.get('Spec')['TaskTemplate']['ContainerSpec']['Image']
                if 'State' in updateStatus: response[service.name]['Status'] = updateStatus['State']
                if 'StartedAt' in updateStatus:response[service.name]['StartedAt'] = updateStatus['StartedAt']

        return response

