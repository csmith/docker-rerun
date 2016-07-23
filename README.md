docker-rerun [![Build Status](https://semaphoreci.com/api/v1/csmith/docker-rerun/branches/master/badge.svg)](https://semaphoreci.com/csmith/docker-rerun)
===============================================================================

`docker-rerun` is a small utility script that makes it easy to re-run docker
containers using the same arguments you used previously.

Want to update to a newer image, or add a missing port publication?
docker-rerun's got you covered.

## Usage

In the most basic usage, you pass in a container name and it will be
stopped, deleted and recreated:

    $ ./docker-rerun apache

You can also pass additional arguments to modify aspects of the container
when it's rerun. For example, to change the image:

    $ ./docker-rerun --image nginx:latest webserver

To check what exactly is going to be performed beforehand, use the --dry-run
option:

    $ ./docker-rerun --dry-run apache
    docker stop apache
    docker rm apache
    docker run --name=apache -p=80:80/tcp --restart=always apache:latest

## What's supported

At present docker-rerun supports copying a number of commonly used arguments:

    * Commands (trailing arguments)
    * Environment variables (-e/--env)
    * Labels (-l/--label)
    * Links (--link)
    * Names (--name)
    * Networks (--net)
    * Port publications (-p)
    * Restart policies (--restart)
    * User switching (-u/--user)
    * Volumes (-v/--volume, and --volumes-from)

If a container uses an argument that's not supported yet, it will be silently
dropped when rerunning.


The following arguments can be used when executing `docker-rerun` to modify
the resulting container:

    * `--image <image>` - changes the image that will be used. You can specify
      tags (`name:tag`) or digests (`name@digest`) as with `docker run`.

## What's not done yet

Many other command line arguments:

    * Network aliases
    * Permissions and policies
    * Advanced networking options

More options to allow mutating the container config when rerunning.

