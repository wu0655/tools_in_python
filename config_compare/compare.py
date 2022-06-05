#!/usr/bin/python3
from ast import Return
import os
import sys


def read_config(path, d):
    with open(path, 'r') as f:
        for line in f.readlines():
            x = line.strip()
            if len(x) == 0 or x.startswith("#"):
                continue
            xx = x.split("=", 1)
            d[xx[0]] = xx[1].strip()


def flush_to_file(d, name):
    fn = open(name, 'w')
    for (key, value) in d.items():
        fn.write(key + " = " + value + '\n')
    fn.close()


def dict_has_item(d, k, v):
    return (k in d.keys()) and (d[k] == v)


class ConfigCompare(object):
    a_dict = {}
    b_dict = {}
    out_a = {}
    out_b = {}
    out_common = {}

    a_file = ""
    b_file = ""

    def __init__(self, path1, path2):
        self.a_file = os.path.realpath(path1)
        self.b_file = os.path.realpath(path2)

    def init(self):
        read_config(self.a_file, self.a_dict)
        read_config(self.b_file, self.b_dict)

    def compare(self):
        # loop. move common in b_dict to common
        for (key, value) in self.a_dict.items():
            if dict_has_item(self.b_dict, key, value):
                self.out_common[key] = value
            else:
                self.out_a[key] = value

        # loop. move common in b_dict to common
        for (key, value) in self.b_dict.items():
            if dict_has_item(self.out_common, key, value):
                pass
            else:
                self.out_b[key] = value

    def output(self):
        flush_to_file(self.out_a, os.path.basename(self.a_file) + ".txt")
        flush_to_file(self.out_b, os.path.basename(self.b_file) + ".txt")
        flush_to_file(self.out_common, "common.txt")


if __name__ == "__main__":
    print('input=' + str(sys.argv))

    if len(sys.argv) < 3:
        print("please input two files")
        sys.exit()

    if not os.path.exists(sys.argv[1]):
        print(sys.argv[1] + "is not exist")
        sys.exit()

    if not os.path.exists(sys.argv[2]):
        print(sys.argv[2] + "is not exist")
        sys.exit()

    cmp = ConfigCompare(sys.argv[1], sys.argv[2])
    cmp.init()
    cmp.compare()
    cmp.output()
