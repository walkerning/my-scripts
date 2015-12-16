#!/bin/python
#-*- coding: utf-8 -*-

import sys
from subprocess import check_output
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('rev', help='git rev')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbose list line numbers of all file blob')

    args = parser.parse_args()

    out = check_output(["git", "ls-tree", "-r", args.rev])
    total_line_num = 0
    for line in out.strip().split('\n'):
        filename = line.replace('\t', ' ').rsplit(' ', 1)[-1]

        line_num_out = check_output(["wc", "-l", filename])
        line_num = int(line_num_out.strip().split(' ', 1)[0])

        total_line_num += line_num
        if args.verbose:
            print '%s: %d' % (filename, line_num)

    log_with_color("Total line number: %d" % total_line_num)

TTY_CSI = '\x1b['
TTY_RESET = '\x1b[0m'

def log_with_color(string):
    isatty =  getattr(sys.stdout, 'isatty', None)
    if isatty and isatty():
        new_string = ''.join([TTY_CSI, ';32m', string, TTY_RESET])
    else:
        new_string = string

    print new_string




if __name__ == "__main__":
    main()
