import os
from lib.base import DockerBasePythonAction

__all__ = [
    'BuildImage'
]


class BuildImage(DockerBasePythonAction):
    def run(self, dockerfile_path, tag):
        # Expand an initial ~ component in the given path
        dockerfile_path = os.path.expanduser(dockerfile_path)

        # Check if the given path was to a Dockerfile or folder
        if os.path.isdir(dockerfile_path):
            fileobj = None
            path = dockerfile_path
            print('Using context directory: %s' % dockerfile_path)
        elif os.path.isfile(dockerfile_path):
            fileobj = open(dockerfile_path, 'rb')
            path = None
            print('Using path to dockerfile: %s' % dockerfile_path)
        else:
            raise Exception('Either dir containing dockerfile or path to dockerfile ' +
                            ' must be provided.')

        opts = self.docker_build_opts
        print('Building docker container. Path = %s, Tag = %s\n' % (dockerfile_path, tag))

        # The build function return a tuple like (image_obj, generator)
        result = self.client.images.build(path=path, fileobj=fileobj, tag=tag, quiet=opts['quiet'],
                                          nocache=opts['nocache'], rm=opts['rm'],
                                          timeout=opts['timeout'])

        image = result[0]
        generator = result[1]
        try:
            for line in generator:
                if 'stream' in line:
                    print(line['stream'])
        except StopIteration:
            pass

        # Check if we need to close the Dockerfile before exiting
        if fileobj is not None:
            fileobj.close()

        return image
