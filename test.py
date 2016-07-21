#!/usr/bin/python3

import subprocess
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
    yield check, ['docker', 'run', '--name=test123', '--net=host', '-d', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '-d', '-p=127.0.0.1:443:443', '-p=127.0.0.1::1336/udp', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '-d', '-p=443', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '--user=root', '-d', 'hello-world', '/hello', 'foobar']
    yield check, ['docker', 'run', '--name=test123', '--net=host', '--user=root:root', '-d', 'hello-world']
    yield check, ['docker', 'run', '--name=test123', '--volume=/dev/null:/null', '--volume=/dev/urandom:/mnt/random', '-d', 'hello-world']
    yield check, ['docker', 'run', '--label=com.example=123 456', '--name=test123', '-d', 'hello-world']
    yield check, ['docker', 'run', '--label=com.example.1', '--label=com.example.2=345', '--name=test123', '-d', 'hello-world']
    yield check, ['docker', 'run', '--link=testA:bar', '--link=testB', '--name=test123', '-d', 'hello-world']


@with_setup(setup_each, teardown_each)
def check(command):
    _run(command)
    output = subprocess.check_output(['./docker-rerun', '--dry-run', 'test123'])
    output = output.decode('utf-8').strip().splitlines()
    assert output[3] == ' '.join(command), 'Expected "%s" but got "%s"' % (' '.join(command), output[3])

