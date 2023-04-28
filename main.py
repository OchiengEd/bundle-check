#!/usr/bin/env python3
from certbundle import Bundle
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        prog='opcheck',
        usage=None,
        description='Operator bundle checking utility',
        add_help=True
    )
    subcmd = parser.add_subparsers()

    bundle_parser = subcmd.add_parser('bundle', 
                                     help='Perform bundle checks')
    bundle_parser.add_argument('-d', 
                              '--directory',
                              nargs='?',
                              help='Bundle directory to check')
    bundle_parser.add_argument('--debug',
                              action='store_true',
                              help='Add debug output')
    bundle_parser.set_defaults(which='bundle')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        
    if len(sys.argv) > 1:
        if args.which == 'bundle':
            bundle_subcommand(args.directory, args.debug)

def bundle_subcommand(directory: str, debug: bool):
    if directory:
        if not os.path.exists(directory):
            sys.exit('error: path not found %s' % directory)
    
    bundle = Bundle(directory, debug)
    bundle.test()

if __name__ == '__main__':
    main()
