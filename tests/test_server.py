from .context import UpdateEndpoint, Authorize
import docker

import unittest
try:
    from unittest import mock
except ImportError:
    import mock

class ServerTestSuite(unittest.TestCase):

    def test_authorize(self):
        self.assertFalse(Authorize('abcd'))
        self.assertTrue(Authorize('DEKU_TEST_TOKEN'))
    
    @mock.patch('deku.server.flask')
    @mock.patch('deku.server.docker')
    def test_update_call(self, mockFlask, mockkDocker):
        mockFlask.Flask = mock.Mock()
        mockFlask.request = mock.Mock()
        mockFlask.request.values = mock.Mock()
        mockClient = mock.Mock()

        def get_arg(arg):
            if arg in args: return args[arg]

        with mock.patch('deku.server.Services', side_effect=lambda base_url=None: mockClient):
            with mock.patch('deku.server.flask.request.values.get', side_effect=get_arg):
                args = { 'name': 'rpc' }
                res = UpdateEndpoint()
                self.assertEqual(res, {'error': 'Invalid secret.'})
                args = { 'name': 'rpc','secret': 'DEKU_TEST_TOKEN' }
                res = UpdateEndpoint()
                mockClient.get_status.assert_called_with(filters={'name': args['name']})
                args['image'] = 'SomeImage'
                res = UpdateEndpoint()
                func_args = { 'update_config': {'image': args['image']}, 'filters': {'name': args['name']} }
                mockClient.update.assert_called_with(**func_args)

if __name__ == '__main__':
    unittest.main()
