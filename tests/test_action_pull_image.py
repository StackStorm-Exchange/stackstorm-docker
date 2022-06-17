import mock
from docker_base_action_test_case import DockerBaseActionTestCase
from pull_image import PullImage

__all__ = [
    'PullImageTestCase'
]


class PullImageTestCase(DockerBaseActionTestCase):
    __test__ = True
    action_cls = PullImage

    def test_init(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, PullImage)

    @mock.patch('lib.base.docker.DockerClient.images')
    def test_run_one_image(self, mock_images):
        action = self.get_action_instance(self.config_good)

        # Declare test variables
        test_repo = 'repo1'
        test_tag = None
        all_tags = None
        test_platform = None
        auth_password_override = None
        auth_username_override = None

        # Mock an image object to use as the return value
        mock_img = mock.Mock()
        mock_images.pull.return_value = mock_img

        expected_result = [mock_img]
        result = action.run(all_tags, auth_password_override, auth_username_override,
                            test_platform, test_repo, test_tag)

        self.assertEqual(result, expected_result)
        mock_images.pull.assert_called_with(test_repo, test_tag, all_tags,
                                            platform=test_platform,
                                            auth_config=None)

    @mock.patch('lib.base.docker.DockerClient.images')
    def test_run_many_images(self, mock_images):
        action = self.get_action_instance(self.config_good)

        # Declare test variables
        test_repo = None
        test_tag = 'tag1'
        all_tags = None
        test_platform = None
        auth_password_override = None
        auth_username_override = None

        # Mock image objects to use as the return value
        mock_img1 = mock.Mock()
        mock_img2 = mock.Mock()
        expected_result = [mock_img1, mock_img2]

        mock_images.pull.return_value = expected_result

        result = action.run(all_tags, auth_password_override, auth_username_override,
                            test_platform, test_repo, test_tag)

        self.assertEqual(result, expected_result)
        mock_images.pull.assert_called_with(test_repo, test_tag, all_tags,
                                            platform=test_platform,
                                            auth_config=None)

    @mock.patch('lib.base.docker.DockerClient.images')
    def test_run_auth_override(self, mock_images):
        action = self.get_action_instance(self.config_good)

        # Declare test variables
        test_repo = 'repo1'
        test_tag = None
        all_tags = None
        test_platform = None
        auth_password_override = 'user'
        auth_username_override = 'pass'
        test_auth_config = {'username': auth_username_override,
                            'password': auth_password_override}

        # Mock an image object to use as the return value
        mock_img = mock.Mock()
        mock_images.pull.return_value = mock_img

        expected_result = [mock_img]
        result = action.run(all_tags, auth_password_override, auth_username_override,
                            test_platform, test_repo, test_tag)

        self.assertEqual(result, expected_result)
        mock_images.pull.assert_called_with(test_repo, test_tag, all_tags,
                                            platform=test_platform,
                                            auth_config=test_auth_config)
