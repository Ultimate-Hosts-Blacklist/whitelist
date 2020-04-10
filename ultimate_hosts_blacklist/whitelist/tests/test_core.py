"""
The whitelisting tool from the Ultimate-Hosts-Blacklist project.

Provide the tests of ultimate_hosts_blacklist.whitelist.core

License:
::


    MIT License

    Copyright (c) 2018, 2019, 2020, 2020 Ultimate-Hosts-Blacklist
    Copyright (c) 2018, 2019, 2020, 2020 Nissar Chababy
    Copyright (c) 2019, 2020 Mitchell Krog

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: disable=protected-access
from unittest import TestCase
from unittest import main as launch_test

from ultimate_hosts_blacklist.whitelist.core import Core


class TestLineFormatter(TestCase):
    """
    Test the (upstream) line formatter.
    """

    def test_comment_line(self):
        """
        Test the case that we meet a commented line.
        """

        given = "# Hello, World!"
        expected = "# Hello, World!"
        actual = Core().format_upstream_line(given)

        self.assertEqual(expected, actual)

    def test_line_ends_with_comment(self):
        """
        Test the case that we meet a line which ends with a comment.
        """

        given = "0.0.0.0 schön.com # Hello, World!"
        expected = "0.0.0.0 xn--schn-7qa.com # Hello, World!"
        actual = Core().format_upstream_line(given)

        self.assertEqual(expected, actual)

        given = "0.0.0.0 schön.com# Hello, World!"
        expected = "0.0.0.0 xn--schn-7qa.com# Hello, World!"
        actual = Core().format_upstream_line(given)

        self.assertEqual(expected, actual)

    def test_line_ends_with_something_else(self):
        """
        Test the case that we meet a line which ends with something
        which is not a comment.
        """

        given = "0.0.0.0 schön.com  Hello, World!"
        expected = "0.0.0.0 xn--schn-7qa.com  Hello, World!"
        actual = Core().format_upstream_line(given)

        self.assertEqual(expected, actual)

    def test_line_without_separator(self):
        """
        Test the case that we meet a line without separator.
        """

        given = "schön.de"
        expected = "xn--schn-7qa.de"
        actual = Core().format_upstream_line(given)

        self.assertEqual(expected, actual)

    def test_line_with_space(self):
        """
        Test the case that we meet a line with a space as separator.
        """

        given = "0.0.0.0     schön.de"
        expected = "0.0.0.0     xn--schn-7qa.de"
        actual = Core().format_upstream_line(given)

        self.assertEqual(expected, actual)

    def test_line_with_tabs(self):
        """
        Test the case that we meet a line with a tabs as separator.
        """

        given = "0.0.0.0\t\t\tschön.de"
        expected = "0.0.0.0\t\t\txn--schn-7qa.de"
        actual = Core().format_upstream_line(given)

        self.assertEqual(expected, actual)


class TestFiltering(TestCase):
    """
    Test of the filtering.
    """

    def test_simple(self):
        """
        Test a simple case.
        """

        secondary_whitelist = ["google.com", None, b"example.org"]
        given = [
            "0.0.0.0    google.com",
            None,
            "0.0.0.0/8",
            "0.0.0.0\t\t\t\t\twww.google.com",
            "0.15.158.25",
            b"10.120.58.75",
            "10.212.54.132200cdn.tt.omtrdc.net",
            "10.212.54.132200cm.everesttech.net",
            "10.212.54.132200ib.adnxs.com",
            "10.212.54.132200paloaltonetworks.d1.sc.omtrdc.net",
            "10.212.54.132200paloaltonetworks.tt.omtrdc.net",
            "10.212.54.132200pixel.everesttech.net",
            "10.212.54.132200sync-tm.everesttech.net",
            "10.212.54.132200sync.jivox.com",
            "10.255.25.12",
            "127.48.15.78",
            "160.41.54.45.rdns.adjust.com",
            "169.254.18.138",
            "172.31.75.92",
            "192.0.0.221",
            "192.0.2.45",
            "192.168.92.85",
            "192.88.99.18",
            "198.19.61.37",
            "198.51.100.39",
            "203.0.113.145",
            "239.54.72.28",
            "248.64.41.183",
            "255.255.255.255",
            "example.org",
            "google.com",
            "http://www.google.com",
            "https://google.com",
            "www.google.com",
        ]

        expected = [
            "10.212.54.132200cdn.tt.omtrdc.net",
            "10.212.54.132200cm.everesttech.net",
            "10.212.54.132200ib.adnxs.com",
            "10.212.54.132200paloaltonetworks.d1.sc.omtrdc.net",
            "10.212.54.132200paloaltonetworks.tt.omtrdc.net",
            "10.212.54.132200pixel.everesttech.net",
            "10.212.54.132200sync-tm.everesttech.net",
            "10.212.54.132200sync.jivox.com",
            "160.41.54.45.rdns.adjust.com",
        ]
        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            multiprocessing=True,
            processes=1,
        ).filter(items=given)

        self.assertEqual(expected, actual)

    def test_simple_with_anti_whitelist(self):
        """
        Test a simple case along with an anti whitelist.
        """

        secondary_whitelist = ["google.com", None]
        anti_whitelist = ["google.com", None]

        given = [
            "0.0.0.0    google.com",
            "0.0.0.0/8",
            None,
            "0.0.0.0\t\t\t\t\twww.google.com",
            "0.15.158.25",
            "10.120.58.75",
            "10.212.54.132200cdn.tt.omtrdc.net",
            "10.212.54.132200cm.everesttech.net",
            "10.212.54.132200ib.adnxs.com",
            "10.212.54.132200paloaltonetworks.d1.sc.omtrdc.net",
            "10.212.54.132200paloaltonetworks.tt.omtrdc.net",
            "10.212.54.132200pixel.everesttech.net",
            "10.212.54.132200sync-tm.everesttech.net",
            "10.212.54.132200sync.jivox.com",
            "10.255.25.12",
            "127.48.15.78",
            "160.41.54.45.rdns.adjust.com",
            "169.254.18.138",
            "172.31.75.92",
            "192.0.0.221",
            "192.0.2.45",
            "192.168.92.85",
            "192.88.99.18",
            "198.19.61.37",
            "198.51.100.39",
            "203.0.113.145",
            "239.54.72.28",
            "248.64.41.183",
            "255.255.255.255",
            "example.org",
            "google.com",
            "http://www.google.com",
            "https://google.com",
            "www.google.com",
        ]

        expected = [
            "0.0.0.0    google.com",
            "0.0.0.0\t\t\t\t\twww.google.com",
            "10.212.54.132200cdn.tt.omtrdc.net",
            "10.212.54.132200cm.everesttech.net",
            "10.212.54.132200ib.adnxs.com",
            "10.212.54.132200paloaltonetworks.d1.sc.omtrdc.net",
            "10.212.54.132200paloaltonetworks.tt.omtrdc.net",
            "10.212.54.132200pixel.everesttech.net",
            "10.212.54.132200sync-tm.everesttech.net",
            "10.212.54.132200sync.jivox.com",
            "160.41.54.45.rdns.adjust.com",
            "example.org",
            "google.com",
            "http://www.google.com",
            "https://google.com",
            "www.google.com",
        ]
        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            anti_whitelist=anti_whitelist,
            multiprocessing=True,
            processes=1,
        ).filter(items=given)

        self.assertEqual(expected, actual)

    def test_simple_without_whitelist(self):
        """
        Test a simple case without a whitelist given.
        """

        given = ["example.org", "google.com", "www.google.com"]
        expected = given
        actual = Core(use_official=False, secondary_whitelist=None).filter(items=given)

        self.assertEqual(expected, actual)

    def test_all(self):
        """
        Test a case with ALL.
        """

        secondary_whitelist = ["google.com", "www.hello.world", "ALL .com"]
        given = [
            "example.org",
            "google.com",
            "www.google.com",
            "github.com",
            "example.com",
            "test.org",
        ]
        expected = ["example.org", "test.org"]
        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            multiprocessing=True,
        ).filter(items=given)

        self.assertEqual(expected, actual)

        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            multiprocessing=True,
        ).filter(items=given, already_formatted=True)

        self.assertEqual(expected, actual)

    def test_all_with_anti_whitelist(self):
        """
        Test a case with ALL.
        """

        secondary_whitelist = ["google.com", "www.hello.world", "ALL .com"]
        anti_whitelist = ["ALL .com"]

        given = [
            "example.org",
            "google.com",
            "www.google.com",
            "github.com",
            "example.com",
            "test.org",
        ]
        expected = ["example.org", "github.com", "example.com", "test.org"]
        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            anti_whitelist=anti_whitelist,
            multiprocessing=True,
        ).filter(items=given)

        self.assertEqual(expected, actual)

        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            anti_whitelist=anti_whitelist,
            multiprocessing=True,
        ).filter(items=given, already_formatted=True)

        self.assertEqual(expected, actual)

    def test_reg(self):
        """
        Test a case with REG.
        """

        secondary_whitelist = ["google.com", "REG g"]
        given = [
            "",
            "example.com",
            "0.0.0.0   example.com",
            "0.0.0.0\t\t\texample.com",
            "example.org",
            "github.com",
            "google.com",
            "test.org",
            "192.168.178.1",
            "www.google.com",
        ]
        expected = ["example.com", "0.0.0.0   example.com", "0.0.0.0\t\t\texample.com"]
        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            multiprocessing=False,
        ).filter(items=given)

        self.assertEqual(expected, actual)

        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            multiprocessing=True,
        ).filter(items=given)

        self.assertEqual(expected, actual)

    def test_reg_with_anti_whitelist(self):
        """
        Test a case with REG.
        """

        secondary_whitelist = ["google.com", "REG g"]
        anti_whitelist = ["REG g"]

        given = [
            "",
            "example.com",
            "0.0.0.0   example.com",
            "0.0.0.0\t\t\texample.com",
            "example.org",
            "github.com",
            "google.com",
            "test.org",
            "192.168.178.1",
            "www.google.com",
        ]
        expected = [
            "example.com",
            "0.0.0.0   example.com",
            "0.0.0.0\t\t\texample.com",
            "example.org",
            "github.com",
            "test.org",
        ]

        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            anti_whitelist=anti_whitelist,
            multiprocessing=False,
        ).filter(items=given)

        self.assertEqual(expected, actual)

        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            anti_whitelist=anti_whitelist,
            multiprocessing=True,
        ).filter(items=given)

        self.assertEqual(expected, actual)

    def test_rzd(self):
        """
        Test a case with RZD.
        """

        secondary_whitelist = ["google.com", "RZD www.example"]
        given = [
            "example.org",
            "example.com",
            "example.co.uk",
            "example.de",
            "example.fr",
            "example.km",
            "www.example.com",
            "example.mg",
        ]
        expected = []
        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            multiprocessing=False,
        ).filter(items=given)

        self.assertEqual(expected, actual)

        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            multiprocessing=True,
        ).filter(items=given, already_formatted=True)

        self.assertEqual(expected, actual)

    def test_rzd_with_anti_whitelist(self):
        """
        Test a case with RZD.
        """

        secondary_whitelist = ["google.com", "RZD example"]
        anti_whitelist = ["RZD example"]

        given = [
            "example.org",
            "example.com",
            "example.co.uk",
            "example.de",
            "example.fr",
            "example.km",
            "www.example.com",
            "example.mg",
        ]
        expected = given

        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            anti_whitelist=anti_whitelist,
            multiprocessing=False,
        ).filter(items=given)

        self.assertEqual(expected, actual)

        actual = Core(
            use_official=False,
            secondary_whitelist=secondary_whitelist,
            anti_whitelist=anti_whitelist,
            multiprocessing=True,
        ).filter(items=given, already_formatted=True)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_test()
