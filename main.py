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


def file_append(filename, contents):
    f = open(filename, "a")
    f.write(contents)
    f.close()


def add_org_item(task, priority, filename):
    item_to_add = '* TODO [#' + priority + '] ' + task
    file_append(filename, item_to_add)
    file_append(filename, '\n')
    print('Added item: ' + item_to_add)


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

    parser.add_argument(
        '-p',
        '--priority',
        metavar = '<priority>',
        nargs = 1,
        type = str,
        default = ['C'],
        help = 'priority filter e.g. A, B'
    )

    parser.add_argument(
        '-a',
        '--add',
        metavar = '<task>',
        nargs = 1,
        type = str,
        default = [None],
        help = 'add task'
    )

    parser.add_argument(
        '-s',
        '--set-priority',
        metavar = '<priority>',
        nargs = 1,
        type = str,
        default = ['B'],
        help = 'priority for new task'
    )

    args = parser.parse_args()

    if args.add != [None]:
        if os.path.exists(args.file[0]) or args.file[0] == default_file:
            add_org_item(args.add[0], args.set_priority[0], args.file[0])
        else:
            print("File not found: " + str(args.file[0]))
        exit()


    if os.path.exists(args.file[0]):
        org_items = (parse_org(args.file[0]))
        # print by priority
        for i in org_items:
            if (i[0][2]) == '[#A]':
                print_todo(i[0])
        if args.priority[0] == 'A':
            exit()
        for i in org_items:
            if (i[0][2]) == '[#B]':
                print_todo(i[0])
        if args.priority[0] == 'B':
            exit()
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
