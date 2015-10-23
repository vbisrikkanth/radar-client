#!/usr/bin/env python

from __future__ import print_function

import argparse
import subprocess
import sys
import os

PURPLE = '\033[95m'
CYAN = '\033[96m'
DARK_CYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


def error(x):
    print(RED + x + END, file=sys.stderr)


def heading(x):
    print(BOLD + '========== ' + x + ' ==========' + END)


def info(x):
    print(BLUE + x + END)


def run_command(args, env=None, cwd=None):
    if cwd is None:
        cwd = os.getcwd()

    if env is None:
        env = {}

    p = subprocess.Popen(args, cwd=cwd, env=env, bufsize=1)
    p.communicate()

    if p.returncode != 0:
        error('Command exited with code %d' % p.returncode)
        raise SystemExit(1)


def run_yum_install(package_name):
    heading('Installing %s...' % package_name)
    return run_command(['sudo', 'yum', 'install', '-y', '-q', package_name])


def run_ansible_playbook(extra_vars=None):
    if extra_vars is None:
      extra_vars = {}

    heading('Running ansible playbook...')

    cmd = ['ansible-playbook', 'site.yml', '-i', '/home/vagrant/ansible/inventory/vagrant_dev']

    if extra_vars:
        for k, v in extra_vars.items():
            info('%s = %s' % (k, v))

        cmd.extend(['--extra-vars', ' '.join('%s=%s' % (k, v) for k, v in extra_vars.items())])

    run_command(cmd, env={
        'HOME': '/home/vagrant',
        'PYTHON_UNBUFFERED': '1',
        'ANSIBLE_FORCE_COLOR': '1'
    })


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pip-index-url', default=None)
    parser.add_argument('--pip-trusted-host', default=None)
    parser.add_argument('--npm-registry', default=None)
    args = parser.parse_args()

    extra_vars = {}

    for key in ['pip_index_url', 'pip_trusted_host', 'npm_registry']:
      value = getattr(args, key)

      if value is not None:
        extra_vars[key] = value

    os.chdir('/home/vagrant/src/ansible')

    run_yum_install('epel-release')
    run_yum_install('ansible')
    run_ansible_playbook(extra_vars)