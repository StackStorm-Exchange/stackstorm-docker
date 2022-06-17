# Docker integration

This package contains some sample docker integrations.

## Actions

### Build image

`docker.build_image` - This action builds a docker image given a path to Dockerfile (could be
directory containing Dockerfile or path to Dockerfile or remote URL containing Dockerfile)
and a tag to use for the image.

### Container exec

`docker.container_exec` - Run a command inside the given container. Similar to docker exec.

### Container get

`docker.container_get` - Return the container object from the given name or ID. Return None if the container does not exist.

### Container run

`docker.container_run` - Run a container. By default, it will wait for the container to finish and return its logs,
similar to docker run.

### Container start

`docker.container_start` - Start the given container. Similar to the docker start command, but doesn’t support attach options.

### Container stop

`docker.container_stop` - Stop the given container.

### Image get

`docker.image_get` - Return the image object from the given name or ID. Return None if the image does not exist.

### Pull docker image

`docker.pull_image` - This action pulls a docker image from docker registry. Image is identified by repository and tag.

### Push docker image

`docker.push_image` - This action pushes an image to a docker registry. Image is identified by repository and tag.

## Sensors

### Docker container spun up/shut down

This sensor watches the list of containers on local box and sends triggers
whenever a new container is spun up or an exisiting one is shut down.

This sensor exposes the following triggers:

* `docker.container_tracker.started` - Dispatched when a new container has
  been detected / started
* `docker.container_tracker.stopped` - Dispatched when an existing container
  has been stopped

## Requirements

1. Python 3.6 or greater
2. docker-ce (version 20.10 or later)
3. pip install docker (5.0.0 or later)

YMMV if you use versions not listed here.

## Configuration

Copy the example configuration in [docker.yaml.example](./docker.yaml.example)
to `/opt/stackstorm/configs/docker.yaml` and edit as required.

These options mirror the options of docker CLI.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## Notes

If you are connecting to the Docker daemon via the Unix socket, you need to
make sure that this socket is accessible to the system user under which
StackStorm processes are running.

For example, if `stanley` is the name of the system user, he should be added to `docker` group like so:

* sudo usermod -a -G docker stanley
* sudo service docker restart

(If you are currently logged on as the user you are trying to add, you will have to logout/log back in.)

There may also be connection issues of the mode for the socket file isn't correct:

* sudo chmod 666 /var/run/docker.sock
