import mock
import docker
from docker_base_action_test_case import DockerBaseActionTestCase
from container_get import ContainerGet

__all__ = [
    'ContainerGetTestCase'
]


class ContainerGetTestCase(DockerBaseActionTestCase):
    __test__ = True
    action_cls = ContainerGet

    def test_init(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, ContainerGet)

    @mock.patch('lib.base.docker.DockerClient.containers')
    def test_run(self, mock_cont):
        action = self.get_action_instance(self.config_good)

        test_container = 'cont1'
        mock_cont.get.return_value = test_container

        result = action.run(test_container)

        self.assertEqual(result, test_container)
        mock_cont.get.assert_called_with(test_container)

    @mock.patch('lib.base.docker.DockerClient.containers')
    def test_run_not_found(self, mock_cont):
        action = self.get_action_instance(self.config_good)

        test_container = 'cont1'
        mock_cont.get.side_effect = docker.errors.NotFound('not found')

        result = action.run(test_container)

        self.assertEqual(result, None)
        mock_cont.get.assert_called_with(test_container)
