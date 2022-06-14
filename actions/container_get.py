import docker

from lib.base import DockerBasePythonAction


__all__ = [
    'ContainerGet'
]


class ContainerGet(DockerBasePythonAction):
    def run(self, container):
        try:
            container = self.client.containers.get(container)
        # If the given container doesn't exist then return None instead of throwing an error.
        # This way we know to build the image instead of wondering if there's a
        # problem with the docker python module.
        except docker.errors.NotFound as e:
            print('No container found with name or ID: %s' % container)
            return None

        return container
