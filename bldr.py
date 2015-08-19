#!/usr/bin/env python3
# coding: utf8

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
        self.debug = False
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
            if t == 'debug':
                self.debug = True
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
            if not self.debug:
                try:
                    subprocess.check_call(cmd)
                except subprocess.CalledProcessError as e:
                    return e.returncode
                return 0
            return -1


def main():
    b = Bldr(open(sys.argv[1], 'r'))
    return b.build()

if __name__ == '__main__':
    sys.exit(main())
