import yaml

from st2tests.base import BaseActionTestCase


class DockerBaseActionTestCase(BaseActionTestCase):
    __test__ = False

    def setUp(self):
        super(DockerBaseActionTestCase, self).setUp()
        self._config_good = self.load_yaml('config_good.yaml')
        self._config_blank = self.load_yaml('config_blank.yaml')

    def tearDown(self):
        super(DockerBaseActionTestCase, self).tearDown()

    def load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))

    @property
    def config_good(self):
        return self._config_good

    @property
    def config_blank(self):
        return self._config_blank

    def test_run_config_blank(self):
        self.assertRaises(TypeError, self.action_cls, self.config_blank)

    def test_run_config_new(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, self.action_cls)
        return action
