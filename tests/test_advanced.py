# -*- coding: utf-8 -*-

from .context import deku

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(deku.hmm())


if __name__ == '__main__':
    unittest.main()
