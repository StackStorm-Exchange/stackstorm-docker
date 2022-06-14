import mock
import docker
from docker_base_action_test_case import DockerBaseActionTestCase
from image_get import ImageGet

__all__ = [
    'ImageGetTestCase'
]


class ImageGetTestCase(DockerBaseActionTestCase):
    __test__ = True
    action_cls = ImageGet

    def test_init(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, ImageGet)

    @mock.patch('lib.base.docker.DockerClient.images')
    def test_run(self, mock_img):
        action = self.get_action_instance(self.config_good)

        test_image = 'img1'
        mock_img.get.return_value = test_image

        result = action.run(test_image)

        self.assertEqual(result, test_image)
        mock_img.get.assert_called_with(test_image)

    @mock.patch('lib.base.docker.DockerClient.images')
    def test_run_not_found(self, mock_img):
        action = self.get_action_instance(self.config_good)

        test_image = 'img1'
        mock_img.get.side_effect = docker.errors.ImageNotFound('not found')

        result = action.run(test_image)

        self.assertEqual(result, None)
        mock_img.get.assert_called_with(test_image)
