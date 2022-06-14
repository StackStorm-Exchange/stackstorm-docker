from lib.base import DockerBasePythonAction

__all__ = [
    'ContainerStart'
]


class ContainerStart(DockerBasePythonAction):
    def run(self, container):
        container = self.client.containers.get(container)

        return container.start()
