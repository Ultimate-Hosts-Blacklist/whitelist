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

            return ("strict", [line, "www.{0}".format(line)])
        return (None, line.strip())

    @classmethod
    def __get_strict_present_bare(cls, parsed):  # pragma: no cover
        """
        Given the output of self.__parse_line(),
        we return the bare (without www.) version
        of the given rule.
        """

        if isinstance(parsed[-1], list):
            if parsed[-1][0].startswith("www."):
                bare = parsed[-1][4:]
            else:
                bare = parsed[-1][0]
        elif parsed[-1].startwith("www."):
            bare = parsed[-1][4:]
        else:
            bare = parsed[-1]

        return bare

    def parse(self, whitelist_list):  # pylint: disable=too-many-branches
        """
        Parse the given whitelist list and return the whitelisting process.

        :param whitelist_list: The content of the whitelist list.
        :type whitelist_list: list

        :return: The list of all processes.
        :rtype: dict
        """

        result = []
        if whitelist_list:
            result = {"strict": {}, "ends": {}, "present": {}, "regex": []}

            for line in whitelist_list:
                parsed = self.__parse_line(line)

                if parsed[0] in ["strict", "present"]:
                    bare = self.__get_strict_present_bare(parsed)
                    index = bare[:4]

                    if index not in result[parsed[0]]:
                        result[parsed[0]][index] = []

                    if parsed[-1] in result[parsed[0]][index]:  # pragma: no cover
                        continue

                    if isinstance(parsed[-1], list):
                        result[parsed[0]][index].extend(parsed[-1])
                    else:  # pragma: no cover
                        result[parsed[0]][index].append(parsed[-1])
                elif parsed[0] == "ends":
                    index = parsed[-1][-3:]

                    if index not in result["ends"]:
                        result["ends"][index] = []

                    if parsed[-1] in result["ends"][index]:  # pragma: no cover
                        continue

                    result["ends"][index].append(parsed[-1])
                elif parsed[0] == "regex":
                    result["regex"].append(parsed[-1])

            if result["regex"]:
                result["regex"] = "({0})".format("|".join(result["regex"]))
            else:
                result["regex"] = ""

        return result
