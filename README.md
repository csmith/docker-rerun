docker-rerun
===============================================================================

`docker-rerun` is a small utility script that makes it easy to re-run docker
containers using the same arguments you used previously.

Want to update to a newer image, or add a missing port publication?
docker-rerun's got you covered.

## How to use

In the most basic usage, you pass in a container name and it will be
stopped, deleted and recreated:

    $ ./docker-rerun apache

To check what exactly is going to be performed beforehand, use the --dry-run
option:

    $ ./docker-rerun --dry-run apache
    docker stop apache
    docker rm apache
    docker run --name=apache -p=80:80/tcp --restart=always apache:latest

