import mock
from docker_base_action_test_case import DockerBaseActionTestCase
from push_image import PushImage

__all__ = [
    'PushImageTestCase'
]


class PushImageTestCase(DockerBaseActionTestCase):
    __test__ = True
    action_cls = PushImage

    def test_init(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, PushImage)

    @mock.patch('builtins.print')
    @mock.patch('lib.base.docker.DockerClient.images')
    def test_run(self, mock_images, mock_print):
        action = self.get_action_instance(self.config_good)

        # Declare test variables
        test_repo = 'repo1'
        test_tag = None
        test_stream = None
        test_decode = None
        auth_password_override = None
        auth_username_override = None

        # Create a test generator object to use as the return value
        test_gen = [{'status': 'print1'}, {'status': 'print2'}]
        mock_images.push.return_value = test_gen

        expected_result = None
        result = action.run(auth_password_override, auth_username_override,
                            test_decode, test_repo, test_stream, test_tag)

        self.assertEqual(result, expected_result)
        mock_images.push.assert_called_with(test_repo, test_tag, stream=test_stream,
                                            auth_config=None, decode=test_decode)
        calls = [mock.call('print1'), mock.call('print2')]
        mock_print.assert_has_calls(calls, any_order=True)

    @mock.patch('builtins.print')
    @mock.patch('lib.base.docker.DockerClient.images')
    def test_run_auth_override(self, mock_images, mock_print):
        action = self.get_action_instance(self.config_good)

        # Declare test variables
        test_repo = 'repo1'
        test_tag = None
        test_stream = None
        test_decode = None
        auth_password_override = 'user'
        auth_username_override = 'pass'
        test_auth_config = {'username': auth_username_override,
                            'password': auth_password_override}

        # Create a test generator object to use as the return value
        test_gen = [{'status': 'print1'}, {'status': 'print2'}]
        mock_images.push.return_value = test_gen

        expected_result = None
        result = action.run(auth_password_override, auth_username_override,
                            test_decode, test_repo, test_stream, test_tag)

        self.assertEqual(result, expected_result)
        mock_images.push.assert_called_with(test_repo, test_tag, stream=test_stream,
                                            auth_config=test_auth_config, decode=test_decode)
        calls = [mock.call('print1'), mock.call('print2')]
        mock_print.assert_has_calls(calls, any_order=True)
