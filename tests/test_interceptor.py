#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/03
#

__all__ = []

import os
import sys

try:
    from . import _config
    from ._config import unittest
except (ValueError, ImportError):
    import _config
    from _config import unittest


def test_suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(eval(c)) for c in __all__])


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.curdir, "..", "src"))
    sys.path.insert(0, os.path.join(os.path.curdir, ".."))
    sys.path.insert(0, os.path.join(os.path.curdir, "src"))
    sys.path.insert(0, os.path.join(os.path.curdir))
    unittest.main(defaultTest='test_suite')
