#!/usr/bin/python3
from ast import Return
import os
import sys

from parse_cmd_file import CmdDescFile
from parse_dtb_file import DtbPreTmpFile
from utils import varname


class BuiltOutParser(object):
    c_set = set()
    h_set = set()
    other_set = set()
    wildcard_set = set()
    out_path = ""
    source_path = ""
    def __init__(self, path):
        self.out_path = os.path.realpath(path)
        self.source_path = os.path.realpath(path + os.sep + "source")

    def init(self):
        for root, dirs, files in os.walk(self.out_path):
            for f in files:
                filepath = os.path.join(root, f)
                if filepath.endswith(".o.cmd"):
                    self.parse_cmd_file(filepath.strip())

    def dtb_pre_parse(self):
        for root, dirs, files in os.walk(self.out_path + os.sep + "arch"):
            for f in files:
                filepath = os.path.join(root, f)
                if filepath.endswith(".d.pre.tmp"):
                    self.parse_dtb_tmp_file(filepath.strip())

    def __handle_path(self, x):
        if x.startswith(os.sep):
            xpath = x.strip()
        else:
            xpath = self.out_path + os.sep + x.strip()

        return xpath

    def __add_to_set(self, src_set, other_set, in_path):
        path = os.path.realpath(in_path)
        if path.startswith(self.source_path) or path.startswith(self.out_path):
            src_set.add(path)
        else:
            other_set.add(path)

    def parse_source(self, source, path):
        # xx = source.split(" ")
        xx = source
        for x in xx:
            xpath = self.__handle_path(x)
            if os.path.exists(xpath):
                self.__add_to_set(self.c_set, self.other_set, xpath)
            else:
                print("parse_source file=" + path)
                print("line=" + xpath)

    def parse_deps(self, deps, path):
        xx = deps
        for x in xx:
            # handle $(wildcard xxx)
            # TODO multi-file in one file.
            yy = x.strip()
            if yy.startswith("$(wildcard"):
                self.wildcard_set.add(yy)
                continue

            # multi file in one, so split first
            y0 = yy.split(" ")
            for y1 in y0:
                y = y1.strip()
                if len(y) == 0:
                    continue

                elif y.startswith(os.sep):
                    self.__add_to_set(self.h_set, self.other_set, y)
                else:
                    xpath = self.out_path + os.sep + y
                    if os.path.exists(xpath):
                        # self.h_set.add(xpath)
                        self.__add_to_set(self.h_set, self.other_set, xpath)
                    else:
                        print("parse_deps file=" + path)
                        print("line=" + xpath)

    def parse_cmd_file(self, path):
        pass
        desc = CmdDescFile(path)
        if len(desc.deps) > 0:
            self.parse_deps(desc.deps, path)
        if len(desc.source) > 0:
            self.parse_source(desc.source, path)

    def parse_dtb_tmp_file(self, path):
        desc = DtbPreTmpFile(path)
        if len(desc.deps) > 0:
            self.parse_deps(desc.deps, path)

    def dump(self):
        print("-------c_set----------")
        for x in self.c_set:
            print(x)
        print("-------h_set----------")
        for x in self.h_set:
            print(x)
        print("-------other_set----------")
        for x in self.other_set:
            print(x)
        print("-------wildcard_set----------")
        for x in self.wildcard_set:
            print(x)

    @staticmethod
    def flush_to_file(in_set, name):
        fn = open(name, 'w')
        for x in in_set:
            fn.write(x + '\n')
        fn.close()

    def output(self):
        self.flush_to_file(sorted(self.c_set), "c_set.txt")
        self.flush_to_file(sorted(self.h_set), "h_set.txt")
        self.flush_to_file(sorted(self.other_set), "other_set.txt")
        self.flush_to_file(sorted(self.wildcard_set), "wildcard_set.txt")


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    print('input=' + os.sep)

    if not os.path.exists(sys.argv[1]):
        print("input parameter error")
        sys.exit()
    else:
        path = os.path.realpath(sys.argv[1])
    xx = BuiltOutParser(path)
    #xx = BuiltOutParser("/data/work/nxp/manual/uout")
    xx.init()
    xx.dtb_pre_parse()
    xx.output()
