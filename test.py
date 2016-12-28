#!/usr/bin/python3

import docker_rerun
import subprocess
from io import StringIO
from nose.tools import with_setup


def _run(cmd):
    subprocess.call(cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)


def setup():
    _run(['docker', 'run', '--name=testA', '-d', 'hello-world'])
    _run(['docker', 'run', '--name=testB', '-d', 'hello-world'])


def teardown():
    _run(['docker', 'rm', '-f', 'testA'])
    _run(['docker', 'rm', '-f', 'testB'])


def setup_each():
    _run(['docker', 'rm', '-f', 'test123'])


def teardown_each():
    _run(['docker', 'rm', '-f', 'test123'])


@with_setup(setup, teardown)
def test_command_matches():
    yield check, ['docker', 'run', '--name=test123', '-d', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '-d', 'hello-world:latest']
    yield check, ['docker', 'run', '--name=test123', '-d', 'hello-world', '/hello', 'world...']
    yield check, ['docker', 'run', '--env=PATH=/root', '--env=Z=X', '--name=test123', '-d', 'hello-world']
    yield check, ['docker', 'run', '--env=FOO=bar baz', '--name=test123', '-d', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '--restart=always', '-d', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '--restart=on-failure:10', '-d', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '--network=host', '-d', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '-d', '-p=127.0.0.1:443:443', '-p=127.0.0.1::1336/udp', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '-d', '-p=443', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '-d', '-p=80:80', '-p=90', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '--user=root', '-d', 'hello-world', '/hello', 'foobar']
    yield check, ['docker', 'run', '--name=test123', '--network=host', '--user=root:root', '-d', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '--volume=/dev/null:/null', '--volume=/dev/urandom:/mnt/random', '-d', 'hello-world']
    yield check, ['docker', 'run', '--label=com.example=123 456', '--name=test123', '-d', 'hello-world']
    yield check, ['docker', 'run', '--label=com.example.1', '--label=com.example.2=345', '--name=test123', '-d', 'hello-world']
    yield check, ['docker', 'run', '--link=testA:bar', '--link=testB', '--name=test123', '-d', 'hello-world']


@with_setup(setup, teardown)
def test_modifiers():
    yield (check,
           ['docker', 'run', '--name=test123', '-d', 'hello-world'],
           ['--image', 'tutum/hello-world'],
           ['docker', 'run', '--name=test123', '-d', 'tutum/hello-world'])
    yield (check,
           ['docker', 'run', '--name=test123', '-d', 'hello-world'],
           ['--image', 'hello-world:latest'],
           ['docker', 'run', '--name=test123', '-d', 'hello-world:latest'])
    yield (check,
           ['docker', 'run', '--name=test123', '-d', 'hello-world'],
           ['--port', '123:456'],
           ['docker', 'run', '--name=test123', '-d', '-p=123:456', 'hello-world'])
    yield (check,
           ['docker', 'run', '--name=test123', '-d', 'hello-world'],
           ['--port', '123:456', '-p', '80'],
           ['docker', 'run', '--name=test123', '-d', '-p=123:456', '-p=80', 'hello-world'])
    yield (check,
           ['docker', 'run', '--name=test123', '-d', 'hello-world'],
           ['--tag', 'latest'],
           ['docker', 'run', '--name=test123', '-d', 'hello-world:latest'])
    yield (check,
           ['docker', 'run', '--name=test123', '-d', 'hello-world'],
           ['--network', 'none'],
           ['docker', 'run', '--name=test123', '--network=none', '-d', 'hello-world'])
    yield (check,
           ['docker', 'run', '--name=test123', '--network=host', '-d', 'hello-world'],
           ['--network', 'none'],
           ['docker', 'run', '--name=test123', '--network=none', '-d', 'hello-world'])
    yield (check,
           ['docker', 'run', '--name=test123', '-d', 'hello-world'],
           ['--label', 'testLabel'],
           ['docker', 'run', '--label=testLabel', '--name=test123', '-d', 'hello-world'])
    yield (check,
           ['docker', 'run', '--label=test', '--name=test123', '-d', 'hello-world'],
           ['--label', 'test2'],
           ['docker', 'run', '--label=test', '--label=test2', '--name=test123', '-d', 'hello-world'])
    yield (check,
           ['docker', 'run', '--label=test=1', '--name=test123', '-d', 'hello-world'],
           ['--label', 'test=2'],
           ['docker', 'run', '--label=test=2', '--name=test123', '-d', 'hello-world'])


@with_setup(setup_each, teardown_each)
def check(command, args=[], expected=None):
    _run(command)
    output = StringIO()
    docker_rerun.main(['--dry-run', 'test123'] + args, output) 
    output = output.getvalue().splitlines()
    expected = ' '.join(expected or command)
    assert output[3] == expected, 'Expected "%s" but got "%s"' % (expected, output[3])

