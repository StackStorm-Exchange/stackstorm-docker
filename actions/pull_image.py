from lib.base import DockerBasePythonAction

__all__ = [
    'PullImage'
]


class PullImage(DockerBasePythonAction):
    def run(self, all_tags, auth_password_override, auth_username_override,
            platform, repo, tag):

        if auth_username_override and auth_password_override:
            auth_config = {}
            auth_config['username'] = auth_username_override
            auth_config['password'] = auth_password_override
        else:
            auth_config = None

        images = self.client.images.pull(repo, tag, all_tags, platform=platform,
                                         auth_config=auth_config)
        # The pull method above returns either an image object or an array of images
        if type(images) is not list:
            images = [images]

        for image in images:
            print('Image ID: ' + str(image.id))
            print('Tags: ' + str(image.tags))

        return images
