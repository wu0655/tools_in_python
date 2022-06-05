# !/usr/bin/env python3

import os
import subprocess
import sys


def get_git_status():
    global l_branch
    global r_branch
    global repo

    on_branch = "On branch"
    your_branch = "Your branch"
    cmd = "git status"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True)
    curr_line = p.stdout.readline()
    while curr_line != b'':
        line = curr_line.strip().decode("utf-8")
        print(line)
        if line.startswith(on_branch):
            l_branch = line[len(on_branch):].strip()

        if line.startswith(your_branch):
            r_info = line.split("'")[1].strip()
            x = r_info.split("/")
            repo = x[0]
            r_branch = x[1]

        curr_line = p.stdout.readline()

    # print("+++++++++++++++++++++++++")
    # print("local branch = " + l_branch)
    # print("remote branch = " + r_branch)
    # print("repo = " + repo)


l_branch = ""
r_branch = ""
repo = ""

if __name__ == "__main__":
    get_git_status()

    if len(l_branch) == 0 or len(r_branch) == 0 or len(repo) == 0:
        print("+++++++++++++++++++++++++")
        print("push information is not enough. please check")
        print("+++++++++++++++++++++++++")
    else:
        push_cmd = "git push " + repo + " " + l_branch + ":refs/for/" + r_branch
        p = subprocess.Popen(push_cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        r = p.wait()
        print("cmd_status = " + str(r))
