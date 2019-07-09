# -*- coding: utf-8 -*-

from .context import deku

import unittest
from unittest.mock import Mock, MagicMock, patch


class ClientTestSuite(unittest.TestCase):
    """Test docker client"""

    @patch('deku.client.logging')
    def test_client(self, logging):
        docker = MagicMock()
        docker.ping.return_value = True
        logging.warn = Mock()

        # Check if client is running
        client = deku.client.Client(docker)
        self.assertTrue(client.is_running())

        # Handle exception when client is not running
        docker.ping = Mock(side_effect=Exception('Docker client is unavailable'))
        self.assertRaises(Exception, client.is_running())
        logging.warn.assert_called_once_with('Docker service is down: Docker client is unavailable')


if __name__ == '__main__':
    unittest.main()
