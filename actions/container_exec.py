from lib.base import DockerBasePythonAction

__all__ = [
    'ContainerExec'
]


class ContainerExec(DockerBasePythonAction):
    def run(self, cmd, container):

        container = self.client.containers.get(container)

        # The exec_run function return a tuple like (exit_code, b'output')
        result = container.exec_run(cmd)
        exit_code = result[0]
        output = result[1].decode('utf-8')

        # The exec_run function does not automaticcaly raise an error if it fails
        if exit_code is not 0:
            raise Exception(output)

        return output
