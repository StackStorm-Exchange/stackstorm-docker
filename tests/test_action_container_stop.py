import mock
from docker_base_action_test_case import DockerBaseActionTestCase
from container_stop import ContainerStop

__all__ = [
    'ContainerStopTestCase'
]


class ContainerStopTestCase(DockerBaseActionTestCase):
    __test__ = True
    action_cls = ContainerStop

    def test_init(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, ContainerStop)

    @mock.patch('lib.base.docker.DockerClient.containers')
    def test_run(self, mock_client):
        action = self.get_action_instance(self.config_good)

        test_container = 'cont1'
        test_result = 'stop'

        mock_cont = mock.Mock()
        mock_client.get.return_value = mock_cont
        mock_cont.stop.return_value = test_result

        result = action.run(test_container)

        self.assertEqual(result, test_result)
        mock_client.get.assert_called_with(test_container)
        mock_cont.stop.assert_called()
