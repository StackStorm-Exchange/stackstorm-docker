import docker
from lib.base import DockerBasePythonAction

__all__ = [
    'ImageGet'
]


class ImageGet(DockerBasePythonAction):
    def run(self, image):
        try:
            image = self.client.images.get(image)
        # If an image doesn't exist then return None instead of throwing an error.
        # This way we know to build the image instead of wondering if there's a
        # problem with the docker python module.
        except docker.errors.ImageNotFound:
            print('No image found with name or ID: %s' % image)
            return None

        return image
