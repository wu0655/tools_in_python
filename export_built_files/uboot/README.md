# u-boot/kernel

## generate filelist
- python3 BuiltOutParser.py /data/work/nxp/manual/u-boot/out

## translate filepath
### merge all files into one
- cat c_set.txt > x
- cat h_set.txt  >> x
### modify path as needed
- cp ../path_translate_by_sed.sh .
- vim path_translate_by_sed.sh
### do translate
- ./path_translate_by_sed.sh x
- x is the output