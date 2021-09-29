#!/usr/bin/env python

# TurboTODO

import os
import sys
import argparse

home = os.path.expanduser('~')
default_file = (home + "/turbotodo.org")
cwd = os.getcwd()


def read_file_to_array(filename):
    content_array = []
    with open(filename) as f:
        for line in f:
            content_array.append(line.strip('\n'))
        return(content_array)


def parse_org(filename):
    result = []
    item = []
    arr = read_file_to_array(filename)
    for i in arr:
        arr2 = i.split(' ')
        if len(arr2) > 2:
            if arr2[0] == '*' and arr2[1] == 'TODO':
                if item == []:
                    item.append(arr2)
                else:
                    result.append(item)
                    item = []
                    item.append(arr2)
            else:
                item.append(arr2)
        else:
            item.append(arr2)
    result.append(item)
    return result


def print_todo(item):
    sys.stdout.write('TODO')
    if len(item) > 3:
        for i in (2, len(item) - 1):
            sys.stdout.write(' | ')
            sys.stdout.write(str(item[i]))
    elif len(item) > 2:
        sys.stdout.write(' | ')
        sys.stdout.write(str(item[2]))
    print()


def main():
    parser = argparse.ArgumentParser(
        description = '''TurboTODO''',
        epilog = '''Copyright (c) Anthony Fadly (18fadly.anthony@gmail.com)'''
    )

    parser.add_argument(
        '-f',
        '--file',
        metavar = '<file>',
        nargs = 1,
        type = str,
        default = [default_file],
        help = 'org file, default: ' + default_file
    )

    args = parser.parse_args()

    if os.path.exists(args.file[0]):
        org_items = (parse_org(args.file[0]))
        # print by priority
        for i in org_items:
            if (i[0][2]) == '[#A]':
                print_todo(i[0])
        for i in org_items:
            if (i[0][2]) == '[#B]':
                print_todo(i[0])
        for i in org_items:
            # Default priority is between B and C
            if (i[0][2]) != '[#A]' and (i[0][2]) != '[#B]' and (i[0][2]) != '[#C]':
                print_todo(i[0])
        for i in org_items:
            if (i[0][2]) == '[#C]':
                print_todo(i[0])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
