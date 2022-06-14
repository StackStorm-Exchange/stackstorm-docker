import six
import docker
import sys
from lib.base import DockerBasePythonAction


__all__ = [
    'DockerExecRunAction'
]


class DockerExecRunAction(DockerBasePythonAction):
    def parse_response(self, result):
        try:
            #result = container.exec_run(cmd, stdout, stderr, stdin, tty, privileged, user,
            #                            detach, stream, socket, environment, workdir, demux)

            result_code = result[0]
            generator = result[1]

            print(generator)
            for line in generator:
                print(line)

            json_output = six.advance_iterator(generator)
            while json_output:
                print(json_output)
                if 'status' in json_output:
                    sys.stdout.write(json_output['status'] + '\n')
                json_output = six.advance_iterator(generator)
        except StopIteration:
            pass
        except Exception as e:
            sys.stderr.write('Error: %s' % (str(e)))
            raise e

    def run(self, cmd, container, demux, detach, environment, image, privileged, socket, stderr,
            stdin, stdout, stream, tty, user, workdir):

        if container is None and image is None:
            raise Exception('ERROR: Either container or image name must be provided.')

        if container:
            try:
                container = self.client.containers.get(container)
            except docker.errors.NotFound:
                sys.stdout.write("Container: %s not found" % container)

            result = container.exec_run(cmd, stdout, stderr, stdin, tty, privileged, user,
                                        detach, stream, socket, environment, workdir, demux)
            print(result.output)
            #self.parse_response(result)

        if image:
            result = self.client.containers.run(image, command=cmd)
            print(result)
