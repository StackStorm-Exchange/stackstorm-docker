from st2common.runners.base_action import Action
import docker

__all__ = [
    'DockerBasePythonAction'
]


class DockerBasePythonAction(Action):
    def __init__(self, config):
        # Assign sane defaults.
        if config['version'] is None:
            config['version'] = '1.13'
        if config['url'] is None:
            config['url'] = 'unix://var/run/docker.sock'

        self._version = config['version']
        self._url = config['url']
        self._timeout = 10
        if config['timeout'] is not None:
            self._timeout = config['timeout']
        self.client = docker.DockerClient(base_url=self._url,
                                          version=self._version,
                                          timeout=self._timeout)
        self.docker_build_opts = config['build_options']
