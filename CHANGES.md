# Change Log

# 2.0.0

- Replaced the depracated docker-py module with newer docker module
- Updated Docker API version from 1.13 to 1.41
- Added the following actions:
  - `container_exec` - Run a command inside the given container. Similar to docker exec.
  - `container_get` - Return the container object from the given name or ID. Return None if the container does not exist
  - `container_run` - Run a container. By default, it will wait for the container to finish and return its logs, similar to docker run
  - `container_start` - Start the given container. Similar to the docker start command, but doesn’t support attach options.
  - `container_stop` - Stop the given container
  - `image_get` - Return the image object from the given name or ID. Return None if the image does not exist
- Added unit tests for all actions

# 1.0.0

* Drop Python 2.7 support

# 0.3.2

- Minor linting fixes

# 0.3.0

- Updated action `runner_type` from `run-python` to `python-script`

# 0.2.0

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.
- Removed `limit` configuration option

# 0.1.0

- First release 
