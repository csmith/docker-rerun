#!/usr/bin/python3

import subprocess
import unittest


class RerunTest(unittest.TestCase):


    def _run(self, cmd):
        subprocess.call(cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)


    def test_command_matches(self):
        commands = [
            'docker run --name=test123 -d hello-world',
            'docker run --name=test123 -d hello-world:latest',
            'docker run --name=test123 -d hello-world /hello world...',
            'docker run --name=test123 --restart=always -d hello-world',
            'docker run --name=test123 --restart=on-failure:10 -d hello-world',
            'docker run --name=test123 --net=host -d hello-world',
            'docker run --name=test123 -d -p=127.0.0.1:443:443/tcp -p=127.0.0.1::1336/tcp hello-world',
            'docker run --name=test123 -d -p=443/tcp hello-world',
            'docker run --name=test123 --volume=/dev/null:/null --volume=/dev/urandom:/mnt/random -d hello-world',
        ]

        for command in commands:
            with self.subTest(cmd=command):
                self._run(['docker', 'rm', '-f', 'test123'])
                self._run(command.split(' '))
                output = subprocess.check_output(['./docker-rerun', '--dry-run', 'test123'])
                output = output.decode('utf-8').strip().splitlines()
                self.assertEqual(output[3], command)
                self._run(['docker', 'rm', '-f', 'test123'])

