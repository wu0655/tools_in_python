#!/usr/bin/python3
import os
import sys
from BuiltOutParser import BuiltOutParser


class VsCodeProj(object):
    shadow_path = ""
    shadow_dir = ""
    out_path = ""
    out_path_len = 0
    source_path = ""
    source_path_len = 0

    ln_set = set()
    mkdir_set = set()

    def __init__(self, path):
        self.out_path = os.path.realpath(path)
        self.out_path_len = len(self.out_path)

    def generate(self, save_list):
        export_info = BuiltOutParser(self.out_path)
        export_info.init()
        export_info.dtb_pre_parse()
        if save_list:
            export_info.output()

        self.source_path = export_info.source_path + os.sep
        # print("source_path=" + self.source_path)
        self.source_path_len = len(self.source_path)

        dir_name = os.path.realpath(export_info.source_path + os.sep + ".." + os.sep)
        # print("dir_name=" + dir_name)
        self.shadow_dir = os.path.basename(export_info.source_path) + "_shadow"
        self.shadow_path = dir_name + os.sep + self.shadow_dir
        # print("shadow_path=" + self.shadow_path)

        for x in export_info.c_set:
            if x.startswith(export_info.source_path):
                self.handle_one_src_file(x)
            elif x.startswith(export_info.out_path):
                self.handle_one_gen_file(x)

        for x in export_info.h_set:
            if x.startswith(export_info.source_path):
                self.handle_one_src_file(x)
            elif x.startswith(export_info.out_path):
                self.handle_one_gen_file(x)

        for x in export_info.other_set:
            y = x.strip()
            if len(y) > 0:
                self.handle_one_other(y)

    def handle_one_src_file(self, src):
        dst = self.shadow_path + os.sep + src[self.source_path_len:len(src)]
        dst_dir = os.path.dirname(dst)
        self.mkdir_set.add("mkdir -p " + dst_dir)
        cmd = "ln -s " + src + " " + dst
        self.ln_set.add(cmd)


    def handle_one_gen_file(self, src):
        dst = self.shadow_path + os.sep + "out" + os.sep + src[self.out_path_len:len(src)]
        dst_dir = os.path.dirname(dst)
        self.mkdir_set.add("mkdir -p " + dst_dir)
        cmd = "ln -s " + src + " " + dst
        self.ln_set.add(cmd)

    def handle_one_other(self, src):
        dst = self.shadow_path + os.sep + "read_only" + os.sep + src
        dst_dir = os.path.dirname(dst)
        self.mkdir_set.add("mkdir -p " + dst_dir)
        cmd = "ln -s " + src + " " + dst
        self.ln_set.add(cmd)

    @staticmethod
    def flush_to_file(in_set, name):
        fn = open(name, 'w')
        for x in in_set:
            fn.write(x + '\n')
        fn.close()


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    print('input=' + os.sep)

    if not os.path.exists(sys.argv[1]):
        print("input parameter error")
        sys.exit()
    else:
        path = os.path.realpath(sys.argv[1])

    xx = VsCodeProj(path)
    xx.generate(True)

    xx.flush_to_file(sorted(xx.mkdir_set), "mkdir_set.sh")
    xx.flush_to_file(sorted(xx.ln_set), "ln_set.sh")
