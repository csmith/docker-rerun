#!/usr/bin/python3

import subprocess
from nose_parameterized import parameterized


def _run(cmd):
    subprocess.call(cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)


@parameterized([
    ['docker', 'run', '--name=test123', '-d', 'hello-world'],
    ['docker', 'run', '--name=test123', '-d', 'hello-world:latest'],
    ['docker', 'run', '--name=test123', '-d', 'hello-world', '/hello', 'world...'],
    ['docker', 'run', '--env=PATH=/root', '--env=Z=X', '--name=test123', '-d', 'hello-world'],
    ['docker', 'run', '--env=FOO=bar baz', '--name=test123', '-d', 'hello-world'],
    ['docker', 'run', '--name=test123', '--restart=always', '-d', 'hello-world'],
    ['docker', 'run', '--name=test123', '--restart=on-failure:10', '-d', 'hello-world'],
    ['docker', 'run', '--name=test123', '--net=host', '-d', 'hello-world'],
    ['docker', 'run', '--name=test123', '-d', '-p=127.0.0.1:443:443/tcp', '-p=127.0.0.1::1336/tcp', 'hello-world'],
    ['docker', 'run', '--name=test123', '-d', '-p=443/tcp', 'hello-world'],
    ['docker', 'run', '--name=test123', '--user=root', '-d', 'hello-world', '/hello', 'foobar'],
    ['docker', 'run', '--name=test123', '--net=host', '--user=root:root', '-d', 'hello-world'],
    ['docker', 'run', '--name=test123', '--volume=/dev/null:/null', '--volume=/dev/urandom:/mnt/random', '-d', 'hello-world'],
    ['docker', 'run', '--label=com.example=123 456', '--name=test123', '-d', 'hello-world'],
    ['docker', 'run', '--label=com.example.1', '--label=com.example.2=345', '--name=test123', '-d', 'hello-world'],
])
def test_command_matches(*command):
    _run(['docker', 'rm', '-f', 'test123'])
    _run(command)
    output = subprocess.check_output(['./docker-rerun', '--dry-run', 'test123'])
    output = output.decode('utf-8').strip().splitlines()
    assert output[3] == ' '.join(command)
    _run(['docker', 'rm', '-f', 'test123'])

