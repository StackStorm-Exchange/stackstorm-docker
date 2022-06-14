import os
import docker
from lib.base import DockerBasePythonAction

__all__ = [
    'ContainerRun'
]


class ContainerRun(DockerBasePythonAction):
    def run(self, cmd, container_name, detach, image, remove):
        result = self.client.containers.run(image, command=cmd, detach=detach,
                                            remove=remove, name=container_name)
        return result
