#!/usr/bin/python3
import os
import sys
from BuiltOutParser import BuiltOutParser

print('input=' + str(sys.argv))
print('input=' + os.sep)

if not os.path.exists(sys.argv[1]):
    print("input parameter error")
    sys.exit()
else:
    path = os.path.realpath(sys.argv[1])

xx = BuiltOutParser(path)

xx.init()
xx.dtb_pre_parse()

