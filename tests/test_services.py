# -*- coding: utf-8 -*-

from .context import Services
import docker

import unittest
try:
    from unittest import mock
except ImportError:
    import mock

class ServicesTestSuite(unittest.TestCase):
    """Test deku services"""

    def test_list_services(self):
        dockerClient = mock.Mock()
        dockerClient.ping.return_value = False
        services = Services(dockerClient)
        # Return empty array when docker is down.
        self.assertEqual(services.get(), [])
        dockerClient.ping.return_value = True
        dockerClient.services.list.return_value = []
        svcs = services.get()
        self.assertEqual(svcs, [])
        dockerClient.services.list.assert_called_with(filters=None)

    def test_update_services_with_no_service_running(self):
        dockerClient = mock.Mock()
        dockerClient.ping.return_value = True
        dockerClient.services = mock.Mock()
        # When there's no service to update
        dockerClient.services.list.return_value = []
        services = Services(dockerClient)
        args = { "filters": {"name":"odin_service"} }
        resp = services.update(**args)
        dockerClient.services.list.assert_called_with(filters=args['filters'])
        self.assertEqual(resp, {'Error': 'No services to update'})

    def test_update_service(self):
        dockerClient = mock.Mock()
        dockerClient.ping.return_value = True
        dockerClient.services = mock.Mock()
        # When there's a service to update
        mockService = mock.Mock()
        mockService.name = 'odin'
        # when updating service runs into an exception
        mockService.update = mock.Mock(side_effect=docker.errors.APIError('Some weird error'))
        dockerClient.services.list.return_value = [mockService]
        services = Services(dockerClient)
        args = {'update_config': {'image': 'repo/image:tag'}}
        resp = services.update(**args)
        self.assertEqual({'odin': {'Message': 'Update failed with error "Some weird error"', 'Status': 'failed'}}, resp)
        # when service update returns no exception
        mockService.update = mock.Mock()
        mockService.attrs.get.return_value = {}
        resp = services.update(**args)
        self.assertEqual({'odin': {'Message': 'Update has been initaited', 'Status': 'updating'}}, resp)

    def test_get_update_status(self):
        dockerClient = mock.Mock()
        dockerClient.ping.return_value = True
        dockerClient.services = mock.Mock()
        # When there's a service to update
        mockService = mock.Mock()
        mockService.name = 'thor'
        service_dict = {'UpdateStatus': {'Message': 'There is always some good in bad', 'Image': 'good', 'State': 'Updating'}, 'Spec': {'TaskTemplate': {'ContainerSpec': {'Image': 'Good'}}}}
        get_attrs = lambda attr: service_dict[attr]
        mockService.attrs.get = mock.MagicMock(side_effect=get_attrs)
        dockerClient.services.list.return_value = [mockService]
        services = Services(dockerClient)
        resp = services.get_status()
        self.assertEqual(resp, {'thor': {'Image': 'Good', 'Message': 'There is always some good in bad', 'Status': 'Updating'}})
        
if __name__ == '__main__':
    unittest.main()
