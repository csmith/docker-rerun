docker-rerun
===============================================================================

[![Build Status](https://semaphoreci.com/api/v1/csmith/docker-rerun/branches/master/shields_badge.svg)](https://semaphoreci.com/csmith/docker-rerun)
[![Code Coverage](https://coveralls.io/repos/github/csmith/docker-rerun/badge.svg)](https://coveralls.io/github/csmith/docker-rerun)
[![PyPI](https://img.shields.io/pypi/v/docker-rerun.svg?maxAge=2592000)](https://pypi.python.org/pypi/docker-rerun)
[![PyPI Downloads](https://img.shields.io/pypi/dm/docker-rerun.svg)](https://pypi.python.org/pypi/docker-rerun)

`docker-rerun` is a small utility script that makes it easy to re-run docker
containers using the same arguments you used previously.

Want to update to a newer image, or add a missing port publication?
docker-rerun's got you covered.

## Installation

You can install the current stable version of docker-rerun using pip:

    $ pip install --upgrade docker-rerun

Or the bleeding edge version from git:

    $ pip install --upgrade git+https://github.com/csmith/docker-rerun.git

Note that `docker-rerun` requires Python 3, so you may need to use `pip3` in
place of `pip` depending on your system configuration.

## Usage

In the most basic usage, you pass in a container name and it will be
stopped, deleted and recreated:

    $ docker-rerun apache

You can also pass additional arguments to modify aspects of the container
when it's rerun. For example, to change the image:

    $ docker-rerun --image nginx:latest webserver

To check what exactly is going to be performed beforehand, use the --dry-run
option:

    $ docker-rerun --dry-run apache
    docker stop apache
    docker rm apache
    docker run --name=apache -p=80:80/tcp --restart=always apache:latest

## Demo

[![asciicast](https://asciinema.org/a/80782.png)](https://asciinema.org/a/80782?speed=2.5&autoplay=1)

## What's supported

At present docker-rerun supports copying a number of commonly used arguments:

 * Commands (trailing arguments)
 * Environment variables (-e/--env)
 * Labels (-l/--label)
 * Links (--link)
 * Names (--name)
 * Networks (--network)
 * Port publications (-p)
 * Restart policies (--restart)
 * User switching (-u/--user)
 * Volumes (-v/--volume, and --volumes-from)

If a container uses an argument that's not supported yet, it will be silently
dropped when rerunning.

## Arguments

The built-in help shows all available arguments. `--dry-run` and `--pull`
affect the behaviour of `docker-rerun`; other options allow modification
of the container's parameters.

    usage: docker-rerun [-h] [-d] [--pull] [--image IMAGE] [--label LABEL]
                        [--network NETWORK] [--port PORT] [--tag TAG]
                        container
    
    Reruns docker containers with different parameters.
    
    positional arguments:
      container             The container to rerun
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --dry-run         Don't actually re-run the container, just print what
                            would happen.
      --pull                Docker pull the image before re-running the container
      --image IMAGE         Image to use in place of the original
      --label LABEL, -l LABEL
                            The new label to add to the container.
      --network NETWORK     The new network configuration to use
      --port PORT, -p PORT  Additional port to expose
      --tag TAG             Image tag (version) to use

## What's not done yet

Many other command line arguments:

 * Network aliases
 * Permissions and policies
 * Advanced networking options

More options to allow mutating the container config when rerunning.

