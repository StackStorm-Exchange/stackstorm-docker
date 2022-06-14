from lib.base import DockerBasePythonAction

__all__ = [
    'ContainerStop'
]


class ContainerStop(DockerBasePythonAction):
    def run(self, container):
        container = self.client.containers.get(container)

        return container.stop()
