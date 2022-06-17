import mock
from docker_base_action_test_case import DockerBaseActionTestCase
from build_image import BuildImage

__all__ = [
    'BuildImageTestCase'
]


class BuildImageTestCase(DockerBaseActionTestCase):
    __test__ = True
    action_cls = BuildImage

    def test_init(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, BuildImage)

    @mock.patch('builtins.print')
    @mock.patch('build_image.os')
    @mock.patch('lib.base.docker.DockerClient.images')
    def test_run_directory(self, mock_images, mock_os, mock_print):
        action = self.get_action_instance(self.config_good)

        # Declare test variables
        test_dockerfile_path = '~/path/to/context'
        test_tag = None
        test_fileobj = None

        # The following options are from the config_good.yaml fixture
        opts_quiet = False
        opts_nocache = False
        opts_rm = True
        opts_timeout = 3600

        full_path = '/full/path/to/context'
        mock_os.path.expanduser.return_value = full_path
        mock_os.path.isdir.return_value = True

        # Mock an image object to use as the return value
        mock_img = mock.Mock()
        test_generator = [{'stream': 'print1'}, {'stream': 'print2'}, {'nostream': 'dontprint'}]
        mock_images.build.return_value = [mock_img, test_generator]

        expected_result = mock_img

        result = action.run(test_dockerfile_path, test_tag)

        self.assertEqual(result, expected_result)
        mock_images.build.assert_called_with(path=full_path, fileobj=test_fileobj, tag=test_tag,
                                             quiet=opts_quiet, nocache=opts_nocache, rm=opts_rm,
                                             timeout=opts_timeout)
        calls = [mock.call('print1'), mock.call('print2')]
        mock_print.assert_has_calls(calls, any_order=True)
        mock_os.path.expanduser.assert_called_with(test_dockerfile_path)
        mock_os.path.isdir.assert_called_with(full_path)

    @mock.patch('builtins.print')
    @mock.patch('build_image.os')
    @mock.patch('build_image.open')
    @mock.patch('lib.base.docker.DockerClient.images')
    def test_run_file(self, mock_images, mock_open, mock_os, mock_print):
        action = self.get_action_instance(self.config_good)

        # Declare test variables
        test_dockerfile_path = '~/path/to/Dockerfile'
        test_tag = None
        test_fileobj = mock.MagicMock()

        # The following options are from the config_good.yaml fixture
        opts_quiet = False
        opts_nocache = False
        opts_rm = True
        opts_timeout = 3600

        full_path = '/full/path/to/Dockerfile'
        mock_os.path.expanduser.return_value = full_path
        mock_os.path.isdir.return_value = False
        mock_os.path.isfile.return_value = True
        mock_open.return_value = test_fileobj

        # Mock an image object to use as the return value
        mock_img = mock.Mock()
        test_generator = [{'stream': 'print1'}, {'stream': 'print2'}, {'nostream': 'dontprint'}]
        mock_images.build.return_value = [mock_img, test_generator]

        expected_result = mock_img

        result = action.run(test_dockerfile_path, test_tag)

        self.assertEqual(result, expected_result)
        mock_images.build.assert_called_with(path=None, fileobj=test_fileobj, tag=test_tag,
                                             quiet=opts_quiet, nocache=opts_nocache, rm=opts_rm,
                                             timeout=opts_timeout)
        calls = [mock.call('print1'), mock.call('print2')]
        mock_print.assert_has_calls(calls, any_order=True)
        mock_os.path.expanduser.assert_called_with(test_dockerfile_path)
        mock_os.path.isdir.assert_called_with(full_path)
        mock_os.path.isfile.assert_called_with(full_path)
        mock_open.assert_called_with(full_path, 'rb')
        test_fileobj.close.assert_called_once()

    @mock.patch('build_image.os')
    def test_run_error(self, mock_os):
        action = self.get_action_instance(self.config_good)

        # Declare test variables
        test_dockerfile_path = '~/path/to/context'
        test_tag = None

        full_path = '/full/path/to/context'
        mock_os.path.expanduser.return_value = full_path
        mock_os.path.isdir.return_value = False
        mock_os.path.isfile.return_value = False

        with self.assertRaises(Exception):
            action.run(test_dockerfile_path, test_tag)
