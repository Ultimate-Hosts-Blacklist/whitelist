"""
The whitelist script of the Ultimate-Hosts-Blacklist project.

Provide the tests of ultimate_hosts_blacklist.whitelist.core

License:
::


    MIT License

    Copyright (c) 2018-2019 Ultimate-Hosts-Blacklist
    Copyright (c) 2018-2019 Nissar Chababy
    Copyright (c) 2019 Mitchell Krog

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


class TestMarkers(TestCase):
    """
    Test if all markers are correct.
    """

    def test_marker_validity(self):
        """
        Test if all markers are present and correct.
        """

        known_markers = {"all": "ALL ", "regex": "REG ", "root_zone_db": "RZD "}

        self.assertEqual(known_markers, Core.MARKERS)


class TestLinks(TestCase):
    """
    Test if the links are correct.
    """

    def test_links_validity(self):
        """
        Test if all links are present and correct.
        """

        known_links = {
            "core": "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/whitelist/master/domains.list",  # pylint: disable=line-too-long
            "root_zone_db": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/iana-domains-db.json",  # pylint: disable=line-too-long
            "public_suffix": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/public-suffix.json",  # pylint: disable=line-too-long
        }

        self.assertEqual(known_links, Core.LINKS)


class TestCoreParser(TestCase):
    """
    Test the parser.
    """

    def test_comment_line(self):
        """
        Test the parser for the case we have a comment line.
        """

        given = "# Hello, World!"
        expected = []
        actual = list(Core()._parse_whitelist_list(given))

        self.assertEqual(expected, actual)

    def test_all(self):
        """
        Test the parser for the ALL marker.
        """

        given = "ALL example.com"
        expected = [r"example\.com$"]
        actual = list(Core()._parse_whitelist_list(given))

        self.assertEqual(expected, actual)

    def test_regex(self):
        """
        Test the parser for the REG marker.
        """

        given = r"REG .*\.example.com$"
        expected = [r".*\.example.com$"]
        actual = list(Core()._parse_whitelist_list(given))

        self.assertEqual(expected, actual)

    def test_normal_www(self):
        """
        Test the parser for a normal entry which starts with :code:`www.`
        """

        given = "www.example.org"
        expected = [
            [
                r"^example\.org$",
                r"\s+example\.org$",
                r"\t+example\.org$",
                r"^www\.example\.org$",
                r"\s+www\.example\.org$",
                r"\t+www\.example\.org$",
            ]
        ]
        actual = list(Core()._parse_whitelist_list(given))

        self.assertEqual(expected, actual)

    def test_normal(self):
        """
        Test the parser fo a normal entry.
        """

        given = "example.org"
        expected = [
            [
                r"^example\.org$",
                r"\s+example\.org$",
                r"\t+example\.org$",
                r"^www\.example\.org$",
                r"\s+www\.example\.org$",
                r"\t+www\.example\.org$",
            ]
        ]
        actual = list(Core()._parse_whitelist_list(given))

        self.assertEqual(expected, actual)


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
        actual = Core()._format_upstream_line(given)

        self.assertEqual(expected, actual)

    def test_line_ends_with_comment(self):
        """
        Test the case that we meet a line which ends with a comment.
        """

        given = "0.0.0.0 schön.com # Hello, World!"
        expected = "0.0.0.0 xn--schn-7qa.com # Hello, World!"
        actual = Core()._format_upstream_line(given)

        self.assertEqual(expected, actual)

        given = "0.0.0.0 schön.com# Hello, World!"
        expected = "0.0.0.0 xn--schn-7qa.com# Hello, World!"
        actual = Core()._format_upstream_line(given)

        self.assertEqual(expected, actual)

    def test_line_ends_with_something_else(self):
        """
        Test the case that we meet a line which ends with something
        which is not a comment.
        """

        given = "0.0.0.0 schön.com  Hello, World!"
        expected = "0.0.0.0 xn--schn-7qa.com  Hello, World!"
        actual = Core()._format_upstream_line(given)

        self.assertEqual(expected, actual)

    def test_line_without_separator(self):
        """
        Test the case that we meet a line without separator.
        """

        given = "schön.de"
        expected = "xn--schn-7qa.de"
        actual = Core()._format_upstream_line(given)

        self.assertEqual(expected, actual)

    def test_line_with_space(self):
        """
        Test the case that we meet a line with a space as separator.
        """

        given = "0.0.0.0     schön.de"
        expected = "0.0.0.0     xn--schn-7qa.de"
        actual = Core()._format_upstream_line(given)

        self.assertEqual(expected, actual)

    def test_line_with_tabs(self):
        """
        Test the case that we meet a line with a tabs as separator.
        """

        given = r"0.0.0.0\t\t\tschön.de"
        expected = r"0.0.0.0\t\t\txn--schn-7qa.de"
        actual = Core()._format_upstream_line(given)

        self.assertEqual(expected, actual)


class TestFiltering(TestCase):
    """
    Test of the filtering.
    """

    def test_simple(self):
        """
        Test a simple case.
        """

        secondary_whitelist = ["google.com"]
        given = ["example.org", "google.com", "www.google.com"]
        expected = ["example.org"]
        actual = Core(use_core=False, secondary_whitelist=secondary_whitelist).filter(
            items=given
        )

        self.assertEqual(expected, actual)

    def test_all(self):
        """
        Test a case with ALL.
        """

        secondary_whitelist = ["google.com", "ALL .com"]
        given = [
            "example.org",
            "google.com",
            "www.google.com",
            "github.com",
            "example.com",
            "test.org",
        ]
        expected = ["example.org", "test.org"]
        actual = Core(use_core=False, secondary_whitelist=secondary_whitelist).filter(
            items=given
        )

        self.assertEqual(expected, actual)

    def test_reg(self):
        """
        Test a case with REG.
        """

        secondary_whitelist = ["google.com", "REG g"]
        given = [
            "example.com",
            "0.0.0.0   example.com",
            r"0.0.0.0\t\t\texample.com",
            "example.org",
            "github.com",
            "google.com",
            "test.org",
            "www.google.com",
        ]
        expected = ["example.com", "0.0.0.0   example.com", r"0.0.0.0\t\t\texample.com"]
        actual = Core(use_core=False, secondary_whitelist=secondary_whitelist).filter(
            items=given
        )

        self.assertEqual(expected, actual)

    def test_rzd(self):
        """
        Test a case with RZD.
        """

        secondary_whitelist = ["google.com", "RZD example"]
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
        actual = Core(use_core=False, secondary_whitelist=secondary_whitelist).filter(
            items=given
        )

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_test()
