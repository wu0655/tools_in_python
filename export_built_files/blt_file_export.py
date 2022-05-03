#!/usr/bin/python3
from ast import Return
import os
import sys

from parse_cmd_file import CmdDescFile
from parse_dtb_file import DtbPreTmpFile
from utils import varname


class Parse(object):

    c_set = set()
    h_set = set()
    other_set = set()
    wildcard_set = set()

    def __init__(self, path):
        self.out_path = path
        self.source_path = os.path.realpath(path + "/source")

    def init(self):
        for root,dirs,files in os.walk(self.out_path):
            for f in files:
                filepath =os.path.join(root, f)
                if filepath.endswith(".o.cmd"):
                    self.parse_cmd_file(filepath.strip())
    
    def dtb_pre_parse(self):
           for root,dirs,files in os.walk(self.out_path + "/" + "arch/"):
            for f in files:
                filepath =os.path.join(root, f)
                if filepath.endswith(".d.pre.tmp"):
                    self.parse_dtb_tmp_file(filepath.strip())     

    def __handle_path(self, x):
        if x.startswith('/'):
            xpath = x.strip()
        else:
            xpath = self.out_path + "/" + x.strip()
        
        return xpath
        
    def parse_source(self, source, path):
        #xx = source.split(" ")
        xx = source
        for x in xx:
            xpath = self.__handle_path(x)
            if os.path.exists(xpath):
                self.c_set.add(xpath)
            else:
                print("file=" + path)
                print("line=" + xpath)

    def parse_deps(self, deps, path):
        ##xx = deps.split("\\")
        xx = deps
        for x in xx:
            y = x.strip()
            if y.startswith("$(wildcard"):
                self.wildcard_set.add(y)
            elif y.startswith('/'):
                self.h_set.add(y)
            else:
                xpath = self.out_path + "/" + y
                if os.path.exists(xpath):
                    self.h_set.add(xpath)
                else:
                    print("file=" + path)
                    print("line=" + xpath)

    
    def parse_cmd_file(self, path):
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

    def __flush_to_file(self, set, name):
        fn = open(name,'w')
        for x in set:
            fn.write(x + '\n')
        fn.close()


    def output(self):
        self.__flush_to_file(sorted(self.c_set), "c_set.txt")
        self.__flush_to_file(sorted(self.h_set), "h_set.txt")
        self.__flush_to_file(sorted(self.other_set), "other_set.txt")
        self.__flush_to_file(sorted(self.wildcard_set), "wildcard_set.txt")

if __name__=="__main__":
    print ('input=' + str(sys.argv))

    if not os.path.exists(sys.argv[1]):
        print("input parameter error")
        sys.exit()
    else:
        path = os.path.realpath(sys.argv[1])

    xx = Parse(path)
    ##xx = Parse("/data/work/nxp/u-boot/uout")
    #xx.parse_cmd_file("/data/work/nxp/u-boot/uout/common/.fdt_support.o.cmd")
    #xx.dump()
    xx.init()
    #xx.dtb_pre_parse()
    xx.output()


