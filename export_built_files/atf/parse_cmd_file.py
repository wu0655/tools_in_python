#!/usr/bin/python3

class ObjDepsFile(object):
    source = set()
    deps = set()

    def __init__(self, path):
        with open(path, 'r') as f:
            xx = ""
            for line in f.readlines():
                x = line.strip()
                if x.endswith("\\"):
                    xx += x
                    continue
                elif len(xx) > 0:
                    # last line of "\"
                    pass

                    if xx.startswith("source_"):
                        self.source = xx.split(":=")[1].strip().split(" ")
                    if xx.startswith("deps_"):
                        self.deps = xx.split(":=")[1].strip().split("\\")
                    xx = ""


if __name__ == "__main__":
    xx = ObjDepsFile("/data/work/nxp/u-boot/uout/./net/.nfs.o.cmd")
    print(xx.source)
    print("")
    print(xx.deps)
