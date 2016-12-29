#!/usr/bin/env python
import argparse
import os
import fnmatch


def file_generator(pattern):
    for root, dirs, files in os.walk("."):
        for item in fnmatch.filter(files, pattern):
            yield item


def entries_generator(item, keyword):
    with open(item, 'r') as f:
        for number, line in enumerate(f, 1):
            if str(keyword) in line:
                yield (number, line)


def grep(pattern, keyword):
    for item in file_generator(pattern):
        for number, line in entries_generator(item, keyword):
            print(
                os.path.join('', item) + ":",
                number,
                line.replace(keyword, '\x1b[31m %s\x1b[0m' % keyword)
            )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern')
    parser.add_argument('keyword')
    args = parser.parse_args()
    grep(args.pattern, args.keyword)
