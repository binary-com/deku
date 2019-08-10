import logging
import docker

class Client:
    def __init__(self, client):
        self.client = client

    def is_docker_running(self):
        try:
            return self.client.ping()
        except docker.errors.APIError as e:
            logging.warn('Docker service is down: %s' % (e))
        return False

