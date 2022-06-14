from lib.base import DockerBasePythonAction


__all__ = [
    'DockerPullImageAction'
]


class DockerPullImageAction(DockerBasePythonAction):
    def run(self, all_tags, auth_password_override, auth_username_override,
            platform, repo, tag):

        if auth_username_override and auth_password_override:
            auth_config = {}
            auth_config['username'] = auth_username_override
            auth_config['password'] = auth_password_override
            return self.pull(repo, tag, platform, all_tags,
                             auth_config=auth_config)
        else:
            return self.pull(repo, tag, platform, all_tags)
