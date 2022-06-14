import mock
from docker_base_action_test_case import DockerBaseActionTestCase
from container_start import ContainerStart

__all__ = [
    'ContainerStartTestCase'
]


class ContainerStartTestCase(DockerBaseActionTestCase):
    __test__ = True
    action_cls = ContainerStart

    def test_init(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, ContainerStart)

    @mock.patch('lib.base.docker.DockerClient.containers')
    def test_run(self, mock_client):
        action = self.get_action_instance(self.config_good)

        test_container = 'cont1'
        test_result = 'start'

        mock_cont = mock.Mock()
        mock_client.get.return_value = mock_cont
        mock_cont.start.return_value = test_result

        result = action.run(test_container)

        self.assertEqual(result, test_result)
        mock_client.get.assert_called_with(test_container)
        mock_cont.start.assert_called()
