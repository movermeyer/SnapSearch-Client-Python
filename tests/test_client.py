#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/05
#

__all__ = ['TestClientInit', 'TestClientRequest', ]

import os
import sys

try:
    from . import _config
    from ._config import unittest
except (ValueError, ImportError):
    import _config
    from _config import unittest


class TestClientInit(unittest.TestCase):
    """
    Tests different ways to initialize a Client object.
    """

    def setUp(self):
        self.api_email = "fantasy@email.com"
        self.api_key = "fantasy_Api_Key"
        self.HTTPS_API = "https://snapsearch.io/api/v1/robot"
        self.NON_HTTPS_API = "http://snapsearch.io/api/v1/robot"
        self.EXTERNAL_CACERT_PEM = _config.save_temp(
            "cacert.pem", _config.DATA_CACERT_PEM.encode("utf-8"))
        self.NON_EXISTENT_PEM = _config.save_temp(
            "no_such_file", b"") + ".pem"
        pass  # void return

    def test_client_init(self):
        # initialize with default arguments
        from SnapSearch import Client
        c = Client(self.api_email, self.api_key, {'test': 1})
        pass  # void return

    def test_client_init_external_api_url(self):
        # initialize with default arguments
        from SnapSearch import Client, SnapSearchError
        # https api url
        c = Client(self.api_email, self.api_key, api_url=self.HTTPS_API)
        # non-https api url
        self.assertRaises(SnapSearchError, Client, self.api_email,
                          self.api_key, api_url=self.NON_HTTPS_API)
        pass  # void return

    def test_client_init_external_ca_path(self):
        from SnapSearch import Client, SnapSearchError
        # existing pem file
        c = Client(self.api_email, self.api_key,
                   ca_path=self.EXTERNAL_CACERT_PEM)
        # non-existent pem file
        self.assertRaises(SnapSearchError, Client, self.api_email,
                          self.api_key, ca_path=self.NON_EXISTENT_PEM)
        pass  # void return

    pass


@unittest.skipIf(not os.environ.get('SNAPSEARCH_API_CREDENTIALS', None) and
                 os.environ.get('TRAVIS', False),
                 "API credentials are required for unsupervised testing")
class TestClientRequest(unittest.TestCase):
    """
    Test Client.request() with different URL's.
    """

    def setUp(self):
        self.BAD_API_URL = "https://non.existent/site"
        self.NORMAL_SITE_URL = "https://snapsearch.io/"
        self.INVALID_SITE_URL = "email:liuyu@opencps.net"
        self.NON_EXISTENT_SITE_URL = "https://www.google.com/non-existent"
        # API credentials
        credentials = os.environ.get('SNAPSEARCH_API_CREDENTIALS', None) or \
            raw_input("API credentials: ")
        credentials = credentials.split(":", 2)
        credentials.append("")  # in case the input does not contain ":"
        self.api_email, self.api_key = credentials[:2]
        pass  # void return

    def test_client_request_bad_api_url(self):
        from SnapSearch import Client, SnapSearchError
        c = Client(self.api_email, self.api_key, api_url=self.BAD_API_URL)
        self.assertRaises(SnapSearchError, c.request, self.NORMAL_SITE_URL)
        pass  # void return

    def test_client_request_normal_site_url(self):
        from SnapSearch import Client
        c = Client(self.api_email, self.api_key)
        r = c.request(self.NORMAL_SITE_URL)
        pass  # void return

    def test_client_request_invalid_site_url(self):
        from SnapSearch import Client
        c = Client(self.api_email, self.api_key)
        r = c.request(self.INVALID_SITE_URL)
        pass  # void return

    def test_client_request_missing_site_url(self):
        from SnapSearch import Client
        c = Client(self.api_email, self.api_key)
        r = c.request(self.NON_EXISTENT_SITE_URL)
        pass  # void return

    pass


def test_suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(eval(c)) for c in __all__])


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.curdir, "..", "src"))
    sys.path.insert(0, os.path.join(os.path.curdir, ".."))
    sys.path.insert(0, os.path.join(os.path.curdir, "src"))
    sys.path.insert(0, os.path.join(os.path.curdir))
    unittest.main(defaultTest='test_suite')
