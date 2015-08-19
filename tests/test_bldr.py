#!/usr/bin/env python3
# coding: utf8
# bldr: py.test %

import unittest
from io import StringIO
from os.path import abspath, dirname, basename, splitext

from bldr import Bldr


TEMPLATE = "# bldr: {}"

EXPANSIONS = {
    '%': __file__,
    '%:p': abspath(__file__),
    '%:h': dirname(__file__) or './',
    '%:p:h': dirname(abspath(__file__)),
    '%:t': basename(__file__),
    '%:p:t': basename(abspath(__file__)),
    '%:r': splitext(__file__)[0],
    '%:e': splitext(__file__)[1],
    '%:p:r': splitext(abspath(__file__))[0],
    '%:p:e': splitext(abspath(__file__))[1],
}


class TestBldr(unittest.TestCase):

    def init(self, filestring):
        self.f = StringIO(filestring)
        self.f.name = __file__
        self.b = Bldr(self.f)

    def test_expansions(self):
        for cmd, expected in EXPANSIONS.items():
            self.init(TEMPLATE.format(cmd))
            result = ' '.join(self.b.cmds)
            self.assertEqual(result, expected)

    def test_contiguous(self):
        self.init("""
            # bldr: whatever
            # bldr: ok man %
            # not bldr
            # bldr: some other thing
        """)
        result = self.b.cmds
        expected = ['whatever', 'ok man ' + __file__]
        self.assertEqual(result, expected)

    def test_disable(self):
        self.init("""
            # bldr: disable
            # bldr: true
        """)
        self.assertFalse(self.b.execute)
        self.assertEqual(self.b.build(), -1)


if __name__ == '__main__':
    unittest.main()
