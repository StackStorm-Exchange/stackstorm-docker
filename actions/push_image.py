from lib.base import DockerBasePythonAction


__all__ = [
    'DockerPushImageAction'
]


class DockerPushImageAction(DockerBasePythonAction):
    def run(self, auth_password_override, auth_username_override,
            decode, repo, stream, tag):
        if auth_username_override and auth_password_override:
            auth_config = {}
            auth_config['username'] = auth_username_override
            auth_config['password'] = auth_password_override
            return self.push(repo, tag, stream, decode,
                             auth_config=auth_config)
        else:
            return self.push(repo, tag, stream, decode)
