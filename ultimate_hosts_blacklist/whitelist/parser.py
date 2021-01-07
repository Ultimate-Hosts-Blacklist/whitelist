"""
The whitelisting tool from the Ultimate-Hosts-Blacklist project.

Provide the whitelist list parser logic.

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
# pylint:disable=too-few-public-methods


from ultimate_hosts_blacklist.helpers import List, Dict
from ultimate_hosts_blacklist.whitelist.configuration import Configuration
from ultimate_hosts_blacklist.whitelist.rzdb import RZDB


class Parser:
    """
    Convert the given whitelist list content into something the system understand.

    :param bool no_complement:
        Forbid us the generation of complements.

        Complements are `www.example.org` if `example.org` is given and vice-versa.
    """

    def __init__(self, no_complement=False):
        self.no_complement = no_complement
        self.rzdb = RZDB().list_format()

    def __parse_all_line(self, line):
        """
        Parse the whitelist list line which starts with the all marker.

        :param str line: The line to parse.
        :return:
            A list of parsed rule or a tuple representing the rule.
        :rtype: list, tuple
        """

        record = line.split(Configuration.markers["all"])[-1].strip()

        if record.startswith("."):
            if record.count(".") > 1:
                if self.no_complement:  # pragma: no cover
                    strict_rule = ("strict", [record[1:]])
                else:
                    strict_rule = ("strict", [record[1:], "www.{0}".format(record[1:])])

                return [
                    ("ends", line.split(Configuration.markers["all"])[-1].strip()),
                    strict_rule,
                ]

            return ("ends", line.split(Configuration.markers["all"])[-1].strip())

        return self.__parse_line(f'{Configuration.markers["all"]} .{record}')

    def __parse_rzdb_line(self, line):
        """
        Parse the whitelist list line which starts with the rzdb marker.

        :param str line: The line to parse.
        :return:
            A tuple representing the rule.
        :rtype: tuple
        """

        bare = line.split(Configuration.markers["root_zone_db"])[-1].strip()

        if not self.no_complement and bare.startswith("www."):
            bare = bare[4:]

        result = ["{0}.{1}".format(bare, x) for x in self.rzdb]

        if not self.no_complement:
            result.extend(["www.{0}".format(x) for x in result])
        result = List(result).format()

        return ("present", result)

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

        if isinstance(line, bytes):
            line = line.decode()

        if line and not line.startswith("#"):
            if line.startswith(Configuration.markers["all"]):
                return self.__parse_all_line(line)

            if line.startswith(Configuration.markers["regex"]):
                return ("regex", line.split(Configuration.markers["regex"])[-1].strip())

            if line.startswith(
                Configuration.markers["root_zone_db"]
            ):  # pragma: no cover
                return self.__parse_rzdb_line(line)

            line = line.strip()

            if not self.no_complement and line.startswith("www."):
                line = line[4:]

            if not self.no_complement:
                return ("strict", [line, "www.{0}".format(line)])
            return ("strict", [line])  # pragma: no cover
        return (None, line)

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

    def __parse_parsed(self, parsed):
        """
        Given the output of __parse_line, we parse its output
        into something our core understand.
        """

        result = {"strict": {}, "ends": {}, "present": {}, "regex": []}

        if parsed[0] in ["strict", "present"]:
            bare = self.__get_strict_present_bare(parsed)
            index = bare[:4]

            if index not in result[parsed[0]]:
                result[parsed[0]][index] = []

            if parsed[-1] in result[parsed[0]][index]:  # pragma: no cover
                return {}

            if isinstance(parsed[-1], list):
                result[parsed[0]][index].extend(parsed[-1])
            else:  # pragma: no cover
                result[parsed[0]][index].append(parsed[-1])
        elif parsed[0] == "ends":
            index = parsed[-1][-3:]

            if index not in result["ends"]:
                result["ends"][index] = []

            if parsed[-1] in result["ends"][index]:  # pragma: no cover
                return {}

            result["ends"][index].append(parsed[-1])
        elif parsed[0] == "regex":
            result["regex"].append(parsed[-1])

        return result

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

                if isinstance(parsed, list):
                    for par in parsed:
                        result = Dict(result).merge(
                            self.__parse_parsed(par), strict=False
                        )
                else:
                    result = Dict(result).merge(
                        self.__parse_parsed(parsed), strict=False
                    )

                for index, value in result.items():
                    if not value:
                        result[index] = {}

            if result["regex"]:
                result["regex"] = "({0})".format("|".join(result["regex"]))
            else:
                result["regex"] = ""

        return result
