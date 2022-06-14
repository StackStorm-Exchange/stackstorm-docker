import mock
from docker_base_action_test_case import DockerBaseActionTestCase
from container_exec import ContainerExec

__all__ = [
    'ContainerExecTestCase'
]


class ContainerExecTestCase(DockerBaseActionTestCase):
    __test__ = True
    action_cls = ContainerExec

    def test_init(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, ContainerExec)

    @mock.patch('lib.base.docker.DockerClient.containers')
    def test_run(self, mock_client):
        action = self.get_action_instance(self.config_good)

        test_container = 'cont1'
        test_cmd = 'ls'
        test_exit_code = 0

        mock_cont = mock.Mock()
        mock_client.get.return_value = mock_cont
        mock_cont.exec_run.return_value = [test_exit_code, b'cont1']

        result = action.run(test_cmd, test_container)

        self.assertEqual(result, test_container)
        mock_client.get.assert_called_with(test_container)
        mock_cont.exec_run.assert_called_with(test_cmd)

    @mock.patch('lib.base.docker.DockerClient.containers')
    def test_run_error(self, mock_client):
        action = self.get_action_instance(self.config_good)

        test_container = 'cont1'
        test_cmd = 'ls'
        test_exit_code = 404

        mock_cont = mock.Mock()
        mock_client.get.return_value = mock_cont
        mock_cont.exec_run.return_value = [test_exit_code, b'error']

        with self.assertRaises(Exception):
            action.run(test_cmd, test_container)
            mock_client.get.assert_called_with(test_container)
            mock_cont.exec_run.assert_called_with(test_cmd)
