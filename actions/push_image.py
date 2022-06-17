from lib.base import DockerBasePythonAction

__all__ = [
    'PushImage'
]


class PushImage(DockerBasePythonAction):
    def run(self, auth_password_override, auth_username_override,
            decode, repo, stream, tag):
        if auth_username_override and auth_password_override:
            auth_config = {}
            auth_config['username'] = auth_username_override
            auth_config['password'] = auth_password_override
        else:
            auth_config = None

        try:
            generator = self.client.images.push(repo, tag, stream=stream, auth_config=auth_config,
                                                decode=decode)
            for line in generator:
                if 'status' in line:
                    print(line['status'])
        except StopIteration:
            pass
