"""
The whitelist script of the Ultimate-Hosts-Blacklist project.

Provide the whitelist list parser logic.

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
# pylint:disable=bad-continuation, too-few-public-methods

from ultimate_hosts_blacklist.helpers import List
from ultimate_hosts_blacklist.whitelist.configuration import Configuration
from ultimate_hosts_blacklist.whitelist.rzdb import RZDB


class Parser:
    """
    Convert the given whitelist list content into something the system understand.
    """

    def __init__(self):
        self.rzdb = RZDB().list_format()

    def __parse_line(self, line):
        """
        Parse the given whitelist list line.

        :param line: The whitelist list line.
        :param line: str

        :return:
            (rule description, subject to match)

            or a list of tuple in the same format.
        :rtype: tuple|list
        """

        if line and not line.startswith("#"):
            if line.startswith(Configuration.markers["all"]):
                return ("ends", line.split(Configuration.markers["all"])[-1].strip())

            if line.startswith(Configuration.markers["regex"]):
                return ("regex", line.split(Configuration.markers["regex"])[-1].strip())

            if line.startswith(
                Configuration.markers["root_zone_db"]
            ):  # pragma: no cover
                bare = line.split(Configuration.markers["root_zone_db"])[-1].strip()

                if bare.startswith("www."):
                    bare = bare[4:]

                result = ["{0}.{1}".format(bare, x) for x in self.rzdb]
                result.extend(["www.{0}".format(x) for x in result])
                result = List(result).format()

                return ("present", result)

            line = line.strip()

            if line.startswith("www."):
                line = line[4:]

            return [("strict", line), ("strict", "www.{0}".format(line))]
        return (None, line.strip())

    def parse(self, whitelist_list):
        """
        Parse the given whitelist list and return the whitelisting process.

        :param whitelist_list: The content of the whitelist list.
        :type whitelist_list: list

        :return: The list of all processes.
        :rtype: list
        """

        result = []

        for line in whitelist_list:
            parsed = self.__parse_line(line)

            if isinstance(parsed, list):
                for data in parsed:
                    result.append(data)
            else:
                result.append(parsed)

        return result
