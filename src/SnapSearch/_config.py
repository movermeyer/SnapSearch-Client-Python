# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

__all__ = ['DEBUG', ]

import os
import sys


# language / package compatibility

try:
    # python 3.x
    from io import BytesIO
except ImportError:
    # python 2.x
    from StringIO import StringIO as BytesIO

try:
    # python 3.x
    from urllib.parse import parse_qs as url_parse_qs
    from urllib.parse import quote as url_quote
    from urllib.parse import urlsplit as url_split
    from urllib.parse import unquote as url_unquote
except ImportError:
    # python 2.x
    from urlparse import parse_qs as url_parse_qs
    from urllib import quote as url_quote
    from urlparse import urlsplit as url_split
    from urllib import unquote as url_unquote

# string literal utilities

# python 3.2 dropped explicit unicode literal, i.e., u"str" being illegal, so
# we need a helper function u("str") to emulate u"str" (see :PEP:`414`).

if sys.version_info[0] == 2:

    def u(s):
        return unicode(s, "unicode_escape")

else:

    def u(s):
        return s


# HTTP does not directly support Unicode. So string variables must either be
# ISO-8859-1 characters, or use :RFC:`2047` MIME encoding (see :PEP:``3333``).

# :PEP:`383`: surrogate escape
enc, esc = sys.getfilesystemencoding(), "surrogateescape"


def unicode_to_wsgi(u):
    return u.encode(enc, esc).decode("iso-8859-1")


def wsgi_to_bytes(s):
    return s.encode("iso-8859-1")

# global debugging flag

DEBUG = ('DEBUG' in os.environ) and ('NDEBUG' not in os.environ)
