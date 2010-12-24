#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse

import panda

def main(args):
    p = panda.Panda()

    if args.cur is not None:
        status = p.update_grub_entries()
        print status

    if args.up is not None:
        status = p.update_grub_entries(args.up[0])
        print status

    if args.check is not None:
        packages = p.get_needed_driver_packages(installable=True)
        print ",".join(packages)



def argument():
    '''Command line parser'''
    parser = argparse.ArgumentParser(description='Pardus Alternative Driver Administration',
                                     prog='panda',
                                     usage='%(prog)s [options]')

    parser.add_argument('-v', '--version',
                         action='version',
                         version='%(prog)s 0.0.1')

    subparsers = parser.add_subparsers(help='Commands')
    parser_cur = subparsers.add_parser('cur', help='Show currently used driver')
    parser_cur.add_argument('cur',
                            nargs='*',
                            help="Show currently used driver")

    parser_update = subparsers.add_parser('up', help='Update grub.conf')
    parser_update.add_argument('up',
                            nargs=1,
                            help="Update grub.conf")

    parser_update = subparsers.add_parser('check', help='Check for installable packages')
    parser_update.add_argument('check',
                            nargs='*',
                            help="Check for installable packages")
    # We have to set them all to false, otherwise optional arguments are not
    # passed to the args() namespace
    parser.set_defaults(cur=None,
                        up=None)

    return parser.parse_args()


if __name__ == '__main__':
    args = argument()
    sys.exit(main(args))
