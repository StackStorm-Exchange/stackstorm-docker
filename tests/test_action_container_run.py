import mock
from docker_base_action_test_case import DockerBaseActionTestCase
from container_run import ContainerRun

__all__ = [
    'ContainerExecTestCase'
]


class ContainerExecTestCase(DockerBaseActionTestCase):
    __test__ = True
    action_cls = ContainerRun

    def test_init(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, ContainerRun)

    @mock.patch('lib.base.docker.DockerClient.containers')
    def test_run(self, mock_cont):
        action = self.get_action_instance(self.config_good)

        test_container_name = 'cont1'
        test_cmd = 'ls'
        test_detach = True
        test_image = 'img1'
        test_remove = False

        return_value = 'run result'
        mock_cont.run.return_value = return_value

        result = action.run(test_cmd, test_container_name, test_detach,
                            test_image, test_remove)

        self.assertEqual(result, return_value)
        mock_cont.run.assert_called_with(test_image, command=test_cmd,
                                         detach=test_detach, remove=test_remove,
                                         name=test_container_name)
