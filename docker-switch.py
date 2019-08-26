#! /usr/bin/env python3

import os
import yaml
import argparse
from yaml import Loader, Dumper

config_file_name = os.environ.get('DOCKER_SWITCH_CONFIG')

parser = argparse.ArgumentParser('Docker context switch')
parser.add_argument('--config', '-c', type=str, default=None)

subparsers = parser.add_subparsers(dest='command')
parser_ls = subparsers.add_parser('ls')
parser_switch = subparsers.add_parser('sw')
parser_default = subparsers.add_parser('default')

parser_switch.add_argument('name')

args = parser.parse_args()

if args.config is not None:
    config_file = args.config

with open(config_file_name, 'r') as config_file:
    config = yaml.load(config_file, Loader=Loader)

contexts = config['contexts']

def export_context(name):
    context = contexts[name]
    print(f"export DOCKER_HOST={context['host']}")
    print(f"export DOCKER_CONFIG={context['path']}")
    print(f"export DOCKER_CERT_PATH={context['path']}")
    print(f"export DOCKER_TLS_VERIFY={int(context['tls'])}")

if args.command == 'ls':
    for name, context in contexts.items():
        print(name)
        for key, value in context.items():
            print(f'{key}: {value}')
elif args.command == 'sw':
    export_context(args.name)
    config['default-context'] = args.name
elif args.command == 'default':
    export_context(config['default-context'])
else:
    raise ValueError()

with open(config_file_name, 'w') as config_file:
    config_yaml = yaml.dump(config, Dumper=Dumper)
    config_file.write(config_yaml)

