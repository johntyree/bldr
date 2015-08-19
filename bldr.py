#!/usr/bin/env python
# coding: utf8
# bldr: disable
# bldr: echo %
# bldr: echo %:p
# bldr: echo %:h
# bldr: echo %:p:h
# bldr: echo %:t
# bldr: echo %:r
# bldr: echo %:e

from __future__ import division, print_function

import os
import re
import subprocess
import sys

bldr_regex = re.compile(r'^\s*\S*\s*bldr:\s*(.*)')


class Bldr(object):

    def __init__(self, f):
        self.f = f
        self.cmds = []
        self.execute = True
        for line in f:
            line = line.strip()
            match = bldr_regex.search(line)
            if match:
                print(match.group(1))
                cmd = self.clean_cmd(match.group(1))
                self.cmds.append(cmd)
            elif self.cmds:
                # Commands must be in a contiguous block
                return

    def clean_cmd(self, cmd):
        toks = cmd.split()
        for i, _ in enumerate(toks):
            t = toks[i]
            if t == 'disable':
                self.execute = False
            if '%' in t:
                toks[i] = toks[i].replace('%', self.f.name)
            if ':p' in t:
                toks[i] = os.path.abspath(toks[i]).replace(':p', '')
            if ':h' in t:
                toks[i] = toks[i].replace(':h', '')
                toks[i] = os.path.dirname(toks[i]) or os.path.curdir
            if ':t' in t:
                toks[i] = toks[i].replace(':t', '')
                toks[i] = os.path.basename(toks[i])
            if ':r' in t:
                toks[i] = toks[i].replace(':r', '')
                toks[i], _ext = os.path.splitext(toks[i])
            if ':e' in t:
                toks[i] = toks[i].replace(':e', '')
                _root, toks[i] = os.path.splitext(toks[i])
        return ' '.join(toks)

    def build(self):
        for cmd in self.cmds:
            print("bldr:", cmd)
            cmd = cmd.split()
            if self.execute:
                if subprocess.call(cmd):
                    return 1
                return 0
            return -1


def main():
    b = Bldr(open(sys.argv[1], 'r'))
    b.build()
    return 0

if __name__ == '__main__':
    main()
