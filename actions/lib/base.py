from st2common.runners.base_action import Action
import sys
import six
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
        self._docker_build_opts = config['build_options']

    def build(self, path=None, fileobj=None, tag=None):
        if path is None and fileobj is None:
            raise Exception('Either dir containing dockerfile or path to dockerfile ' +
                            ' must be provided.')
        if path is not None and fileobj is not None:
            sys.stdout.write('Using path to dockerfile: %s\n' % fileobj)
        opts = self._docker_build_opts
        sys.stdout.write('Building docker container. Path = %s, Tag = %s\n' % (path, tag))
        result = self.client.images.build(path=path, fileobj=fileobj, tag=tag, quiet=opts['quiet'],
                                          nocache=opts['nocache'], rm=opts['rm'],
                                          timeout=opts['timeout'])

        generator = result[1]
        try:
            json_output = six.advance_iterator(generator)
            while json_output:
                if 'stream' in json_output:
                    sys.stdout.write(json_output['stream'] + '\n')
                json_output = six.advance_iterator(generator)
        except StopIteration:
            pass
        except Exception as e:
            sys.stderr.write('Error: %s' % (str(e)))
            raise e

    def push(self, repo, tag, stream, decode, auth_config=None):
        try:
            generator = self.client.images.push(repo, tag, stream=stream, auth_config=auth_config,
                                                decode=decode)
            json_output = six.advance_iterator(generator)
            while json_output:
                if 'status' in json_output:
                    sys.stdout.write(json_output['status'] + '\n')
                json_output = six.advance_iterator(generator)
        except StopIteration:
            pass
        except Exception as e:
            sys.stderr.write('Error: %s' % (str(e)))
            raise e

    def pull(self, repo, tag, platform, all_tags, auth_config=None):
        try:
            images = self.client.images.pull(repo, tag, all_tags, platform=platform,
                                             auth_config=auth_config)
            # The pull method above returns either an image object or an array of images
            if type(images) is not list:
                images = [images]

            for image in images:
                sys.stdout.write('Image ID: ' + str(image.id) + '\n')
                sys.stdout.write('Tags: ' + str(image.tags) + '\n')

            return images
        except Exception as e:
            sys.stderr.write('Error: %s' % (str(e)))
            raise e
