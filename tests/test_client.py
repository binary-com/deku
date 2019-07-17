from .context import Client
import docker

import unittest
try:
    from unittest import mock
except ImportError:
    import mock

class ClientTestSuite(unittest.TestCase):
    """Test deku client"""

    @mock.patch('deku.client.logging')
    def test_client(self, logging=None):
        dockerClient = mock.Mock()
        dockerClient.ping.return_value = True
        logging.warn = mock.Mock()

        # Check if client is running
        client = Client(dockerClient)
        self.assertTrue(client.is_docker_running())

        # Handle docker api-error exception
        dockerClient.ping = mock.Mock(side_effect=docker.errors.APIError('Docker client is unavailable'))
        client.is_docker_running()
        logging.warn.assert_called_with('Docker service is down: Docker client is unavailable')

if __name__ == '__main__':
    unittest.main()
