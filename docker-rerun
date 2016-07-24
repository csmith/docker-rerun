#!/usr/bin/python3
"""Re-runs a docker container using the same arguments as before.

Given the name of a container, the previous arguments are determined
and reconstructed by looking at the `docker inspect` output.

Each function named `handle_*` handles one configuration option,
reading the relevant information from the inspect output and adding
the relevant command line flags to the config.

Each function named `modify_*` allows the user to modify the
configuration in some manner. Modify functions are called twice:
once with an ArgumentParser, and subsequently with the parsed
arguments and the container object.
"""

import argparse
import inspect
import json
import subprocess
import sys


class Container(object):
    """Encapsulates information about a container."""

    def __init__(self, container_info, image_info):
        """Creates a new Container.

        Args:
            name (str): The name of the container.
            container_info (dict): Dictionary describing the container state.
            image_info (dict): Dictionary describing the image state.
        """
        self.args = ['-d']
        """The arguments passed to docker to create the container."""

        self.image = ''
        """The image that the container uses."""

        self.cmd = []
        """The command executed within the container."""

        self.info = container_info
        """The container information as returned by `docker inspect`"""

        self.image_info = image_info
        """The image information as returned by `docker inspect`"""


    def command_line(self):
        """Gets the full command-line used to run this container."""
        return ['docker', 'run'] + sorted(self.args) + [self.image] + self.cmd


    def add_args_from_list(self, template, selector):
        """Adds an argument for each item in a list.

        Args:
            template (str): Template to use for the argument. Use %s for value.
            selector (func): Function to extract the list from our info.
        """
        target = selector(self.info)
        if target:
            self.args.extend([template % entry for entry in target])


    def if_image_diff(self, selector, fallback):
        """Gets a property if it's different from the image's config.

        Compares the value of a property in the container's information to the
        same property in the image information. If the value is different then
        the container's version is returned, otherwise the specified fallback
        is returned.

        This is useful where the container inherits config from the image,
        such as the command or the user to run as. We only want to include it
        in the arguments if it has been explicitly changed.

        Args:
            selector (func): Function to extract the property.
            fallback (object): Value to return if the properties are identical.
        """
        container = selector(self.info)
        image = selector(self.image_info)
        return fallback if container == image else container


def docker_inspect(target, what):
    """Uses `docker inspect` to get details about the given container or image.

    Args:
        target (str): The name of the container or image to inspect.
        what (str): The type of object to inspect ('container' or 'image').

    Returns:
        dict: Detailed information about the  target.

    Raises:
        CalledProcessError: An error occurred talking to Docker.
    """
    output = subprocess.check_output(['docker', 'inspect',
                                      '--type=%s' % what, target])
    return json.loads(output.decode('utf-8'))[0]


def handle_binds(container):
    """Copies the volume bind (--volume/-v) arguments."""
    container.add_args_from_list('--volume=%s',
                                 lambda c: c['HostConfig']['Binds'])


def handle_command(container):
    """Copies the command (trailing arguments)."""
    container.cmd = container.if_image_diff(lambda c: c['Config']['Cmd'], [])


def handle_environment(container):
    """Copies the environment (-e/--env) arguments."""
    container_env = set(container.info['Config']['Env'] or [])
    image_env = set(container.image_info['Config']['Env'] or [])
    delta = container_env - image_env
    container.args.extend(['--env=%s' % env for env in delta])


def handle_image(container):
    """Copies the image argument."""
    container.image = container.info['Config']['Image']


def handle_labels(container):
    """Copies the label (-l/--label) arguments."""
    container_labels = set((container.info['Config']['Labels'] or {}).items())
    image_labels = set((container.image_info['Config']['Labels'] or {}).items())
    delta = container_labels - image_labels
    for key, value in delta:
        if value:
            container.args.append('--label=%s=%s' % (key, value))
        else:
            container.args.append('--label=%s' % key)


def handle_links(container):
    """Copies the link (--link) arguments."""
    name = container.info['Name']
    links = container.info['HostConfig']['Links'] or []
    for link in links:
        (target, alias) = link.split(':')
        target = target[1:]
        alias = alias[len(name) + 1:]
        if alias == target:
            container.args.append('--link=%s' % target)
        else:
            container.args.append('--link=%s:%s' % (target, alias))


def handle_name(container):
    """Copies the name (--name) argument."""
    # Trim the leading / off the name. They're equivalent from docker's point
    # of view, but having the plain name looks nicer from a human point of view.
    container.args.append('--name=%s' % container.info['Name'][1:])


def handle_network_mode(container):
    """Copies the network mode (--net) argument."""
    network = container.info['HostConfig']['NetworkMode']
    if network != 'default':
        container.args.append('--net=%s' % network)


def handle_ports(container):
    """Copies the port publication (-p) arguments."""
    ports = container.info['HostConfig']['PortBindings']
    if ports:
        for port, bindings in ports.items():
            # /tcp is the default - no need to include it
            port_name = port[:-4] if port.endswith('/tcp') else port
            for binding in bindings:
                if binding['HostIp']:
                    container.args.append('-p=%s:%s:%s' % (binding['HostIp'],
                                                           binding['HostPort'],
                                                           port_name))
                elif binding['HostPort']:
                    container.args.append('-p=%s:%s' % (binding['HostPort'],
                                                        port_name))
                else:
                    container.args.append('-p=%s' % port_name)


def handle_restart(container):
    """Copies the restart policy (--restart) argument."""
    policy = container.info['HostConfig']['RestartPolicy']
    if policy and policy['Name'] != 'no':
        arg = '--restart=%s' % policy['Name']
        if policy['MaximumRetryCount'] > 0:
            arg += ':%s' % policy['MaximumRetryCount']
        container.args.append(arg)


def handle_user(container):
    """Copies the user (--user/-u) argument."""
    user = container.if_image_diff(lambda c: c['Config']['User'], None)
    if user:
        container.args.append('--user=%s' % user)


def handle_volumes_from(container):
    """Copies the volumes from (--volumes-from) argument."""
    container.add_args_from_list('--volumes-from=%s',
                                 lambda c: c['HostConfig']['VolumesFrom'])


def modify_image(parser=None, args=None, container=None):
    """Allows the image (name, version, etc) to be modified in one go."""
    if parser:
        parser.add_argument('--image',
                            help='Image to use in place of the original')
    elif args.image:
        container.image = args.image


def modify_port_add(parser=None, args=None, container=None):
    """Allows a additional ports to be exposed."""
    if parser:
        parser.add_argument('--port', '-p', action='append',
                            help='Additional port to expose')
    elif args.port:
        container.args.extend(['-p=%s' % port for port in args.port])


def modify_tag(parser=None, args=None, container=None):
    """Allows the tag (version) to be updated."""
    if parser:
        parser.add_argument('--tag',
                            help='Image tag (version) to use')
    elif args.tag:
        # Get rid of any existing digest or tag
        image = container.image.replace('@', ':')
        image = image.split(':')[0]
        container.image = '%s:%s' % (image, args.tag)


def functions():
    """Lists all functions defined in this module.

    Returns:
        list of (str,function): List of (name, function) pairs for each
        function defined in this module.
    """
    return [m for m
            in inspect.getmembers(sys.modules[__name__])
            if inspect.isfunction(m[1])]


def handlers():
    """Lists all handlers defined in this module.

    Returns:
        list of function: All handlers (handle_* funcs) defined in this module.
    """
    return [func for (name, func) in functions() if name.startswith('handle_')]


def modifiers():
    """Lists all modifiers defined in this module.

    Returns:
        list of function: All modifiers (modify_* funcs) in this module.
    """
    return [func for (name, func) in functions() if name.startswith('modify_')]


def main():
    """Script entry point."""
    parser = argparse.ArgumentParser(description='Reruns docker containers ' \
                                                 'with different parameters.')
    parser.add_argument('container', type=str, help='The container to rerun')
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help='Don\'t actually re-run the container, just ' \
                             'print what would happen.')
    parser.add_argument('--pull', action='store_true',
                        help='Docker pull the image before re-running the ' \
                             'container')

    mods = modifiers()
    for mod in mods:
        mod(parser=parser)

    args = parser.parse_args()
    container_info = docker_inspect(args.container, 'container')
    image_info = docker_inspect(container_info['Config']['Image'], 'image')
    container = Container(container_info, image_info)

    for handler in handlers():
        handler(container)

    for mod in mods:
        mod(args=args, container=container)

    commands = [
        ['docker', 'stop', args.container],
        ['docker', 'rm', args.container],
        container.command_line(),
    ]

    if args.pull:
        commands = [['docker', 'pull', container.image]] + commands

    if args.dry_run:
        print('Performing dry run for container %s. The following would be ' \
              'executed:' % args.container)
        for command in commands:
            print(' '.join(command))
    else:
        print('Re-running container %s...' % args.container)
        for command in commands:
            subprocess.check_call(command)


if __name__ == "__main__":
    main()
