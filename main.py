#!/usr/bin/env python

# TurboTODO

import os
import sys
import argparse

home = os.path.expanduser('~')
default_file = (home + "/turbotodo.org")
cwd = os.getcwd()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def flatten(array):
    if isinstance(array, str):
        return array
    result = ""
    for i in array:
        result += i
        result += " "
    return result[:-1]


def add_org_item(task, priority, filename, tag, comment):
    item_to_add = '\n* TODO [#' + priority + '] ' + task
    if tag != None:
        item_to_add += ' :' + tag[0] + ':'
    item_to_add += '\n'
    if comment != None:
        item_to_add += comment[0]
    file_append(filename, item_to_add)
    print('Added item: ' + item_to_add)


def parse_org(filename):
    result = []
    item = []
    arr = read_file_to_array(filename)
    for i in range(1, len(arr)):
        arr2 = arr[i].split(' ')
        if len(arr2) > 2:
            if arr2[0] == '*' and arr2[1] == 'TODO':
                if item == []:
                    item.append(arr2)
                else:
                    result.append(item)
                    item = []
                    item.append(arr2)
                    if i < len(arr) - 1:
                        item.append(arr[i + 1])
            else:
                item.append(arr2)
        else:
            item.append(arr2)
    result.append(item)
    return result


def print_todo(item):
    sys.stdout.write(bcolors.OKCYAN + "TODO")
    for i in range(2, len(item[0])):
        sys.stdout.write(' ')
        sys.stdout.write(bcolors.OKGREEN + item[0][i])
    if len(item) > 1:
        sys.stdout.write('\n>    ')
        sys.stdout.write(bcolors.WARNING + flatten(item[1]))
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

    parser.add_argument(
        '-t',
        '--tag',
        metavar = '<tag>',
        nargs = 1,
        type = str,
        help = 'Tag to add or search'
    )

    parser.add_argument(
        '-c',
        '--comment',
        metavar = '<comment>',
        nargs = 1,
        type = str,
        help = 'comment to append to todo item'
    )

    args = parser.parse_args()

    if args.add != [None]:
        add_org_item(args.add[0], args.set_priority[0], args.file[0], args.tag, args.comment)
        exit()


    if os.path.exists(args.file[0]):
        if args.tag == None:
            org_items = parse_org(args.file[0])
        else:
            org_items = []
            for i in parse_org(args.file[0]):
                if ':' + args.tag[0] + ':' in i[0]:
                    org_items.append(i)
        # print by priority
        for i in org_items:
            if (i[0][2]) == '[#A]':
                print_todo(i)
        if args.priority[0] == 'A':
            exit()
        for i in org_items:
            if (i[0][2]) == '[#B]':
                print_todo(i)
        if args.priority[0] == 'B':
            exit()
        for i in org_items:
            # Default priority is between B and C
            if (i[0][2]) != '[#A]' and (i[0][2]) != '[#B]' and (i[0][2]) != '[#C]':
                print_todo(i)
        for i in org_items:
            if (i[0][2]) == '[#C]':
                print_todo(i)
    else:
        print("File not found: " + str(args.file[0]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
