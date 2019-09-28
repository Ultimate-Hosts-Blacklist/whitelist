"""
The whitelisting tool from the Ultimate-Hosts-Blacklist project.

Provide the tests of ultimate_hosts_blacklist.whitelist.parser

License:
::


    MIT License

    Copyright (c) 2018, 2019 Ultimate-Hosts-Blacklist
    Copyright (c) 2018, 2019 Nissar Chababy
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
from unittest import TestCase
from unittest import main as launch_test

from ultimate_hosts_blacklist.whitelist.parser import Parser


class TestParser(TestCase):
    """
    Test if all configuration are correct.
    """

    def setUp(self):
        """
        Setup everything needed for the tests.
        """

        self.parser = Parser()

    def test_comment_line(self):
        """
        Test the parser for the case we have a comment line.
        """

        given = ["# Hello, World!"]
        expected = {"strict": {}, "ends": {}, "present": {}, "regex": ""}
        actual = self.parser.parse(given)

        self.assertEqual(expected, actual)

    def test_all(self):
        """
        Test the parser for the ALL marker.
        """

        given = ["ALL example.com", "ALL .com"]
        expected = {
            "strict": {"exam": ["example.com", "www.example.com"]},
            "ends": {"com": [".example.com", ".com"]},
            "present": {},
            "regex": "",
        }
        actual = self.parser.parse(given)

        self.assertEqual(expected, actual)

    def test_regex(self):
        """
        Test the parser for the REG marker.
        """

        given = [r"REG .*\.example.com$"]
        expected = {
            "strict": {},
            "ends": {},
            "present": {},
            "regex": r"(.*\.example.com$)",
        }
        actual = self.parser.parse(given)

        self.assertEqual(expected, actual)

    def test_normal_www(self):
        """
        Test the parser for a normal entry which starts with :code:`www.`
        """

        given = ["www.example.org"]
        expected = {
            "strict": {"exam": ["example.org", "www.example.org"]},
            "ends": {},
            "present": {},
            "regex": "",
        }
        actual = self.parser.parse(given)

        self.assertEqual(expected, actual)

    def test_normal(self):
        """
        Test the parser for a normal entry.
        """

        given = ["example.org"]
        expected = {
            "strict": {"exam": ["example.org", "www.example.org"]},
            "ends": {},
            "present": {},
            "regex": "",
        }
        actual = self.parser.parse(given)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_test()
