"""
The whitelisting tool from the Ultimate-Hosts-Blacklist project.

Provide the tests of ultimate_hosts_blacklist.whitelist.configuration

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

from ultimate_hosts_blacklist.whitelist.configuration import Configuration


class TestConfiguration(TestCase):
    """
    Test if all configuration are correct.
    """

    def test_marker_validity(self):
        """
        Test if all markers are present and correct.
        """

        known_markers = {"all": "ALL ", "regex": "REG ", "root_zone_db": "RZD "}

        self.assertEqual(known_markers, Configuration.markers)

    def test_links_validity(self):
        """
        Test if all links are present and correct.
        """

        known_links = {
            "core": "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/whitelist/master/domains.list",  # pylint: disable=line-too-long
            "root_zone_db": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/iana-domains-db.json",  # pylint: disable=line-too-long
            "public_suffix": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/public-suffix.json",  # pylint: disable=line-too-long
        }

        self.assertEqual(known_links, Configuration.links)


if __name__ == "__main__":
    launch_test()
