#!/usr/bin/python3

class DtbPreTmpFile(object):
    deps = set()
    def __init__(self, path):
        with open(path, 'r') as f:
            xx = ""
            for line in f.readlines():
                x = line.strip()
                xx += x
                if (x.endswith("\\")):
                    pass
                else:
                    tmp = xx.split(":")[1].strip().split("\\")
                    for t in tmp:
                        if t.endswith(".h") or t.endswith(".c") or t.endswith(".dtsi") or t.endswith(".dts"):
                            self.deps.add(t)

                    xx=""


if __name__=="__main__":
    xx = DtbPreTmpFile("/data/work/nxp/u-boot/uout/arch/arm/dts/.fsl-s32g274aevb.dtb.d.pre.tmp")
    print(xx.deps)

