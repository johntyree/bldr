#!/usr/bin/env python
# coding: utf8

from __future__ import division, print_function

import os
import re
import subprocess
import sys

bldr_regex = re.compile(r'\s*bldr:\s*(.*)')


class Bldr(object):

    def __init__(self, fn):
        self.fn = fn
        self.cmds = []
        for line in fn:
            line = line.strip()
            match = bldr_regex.search(line)
            if match:
                cmd = self.clean_cmd(match.group(1))
                self.cmds.append(cmd)

    def clean_cmd(self, cmd):
        toks = cmd.split()
        for i, _ in enumerate(toks):
            t = toks[i]
            if t.find('%') != -1:
                toks[i] = self.fn.name
            if t.find(':p') != -1:
                toks[i] = os.path.abspath(toks[i]).replace(':p', '')
            if t.find(':r') != -1:
                toks[i].replace(':r', '')
                toks[i], ext = os.path.splitext(toks[i])
        return ' '.join(toks)

    def build(self):
        for cmd in self.cmds:
            print("bldr:", cmd)
            cmd = cmd.split()
            if subprocess.call(cmd):
                return 1


def main():
    b = Bldr(open(sys.argv[1], 'r'))
    b.build()
    return 0

if __name__ == '__main__':
    main()
