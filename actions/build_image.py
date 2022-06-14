import os

from lib.base import DockerBasePythonAction


__all__ = [
    'DockerBuildImageAction'
]


class DockerBuildImageAction(DockerBasePythonAction):
    def run(self, dockerfile_path, tag):
        if os.path.isdir(dockerfile_path):
            return self.build(path=dockerfile_path, tag=tag)
        else:
            dockerfile_path = os.path.expanduser(dockerfile_path)
            with open(dockerfile_path, 'rb') as fp:
                return self.build(fileobj=fp, tag=tag)
