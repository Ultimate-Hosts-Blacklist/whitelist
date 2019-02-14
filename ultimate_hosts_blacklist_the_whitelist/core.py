"""
The whitelist script of the Ultimate-Hosts-Blacklist project.

Provide the main logic.

License:
::


    MIT License

    Copyright (c) 2018-2019 Nissar Chababy

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
from json import loads

from domain2idna import get as domain2idna

# pylint: disable=bad-continuation
from ultimate_hosts_blacklist_the_whitelist.helpers import (Download, File,
                                                            List, Regex,
                                                            escape)


class Core:  # pylint: disable=too-few-public-methods
    """
    Brain of our system.
    """

    MAKERS = {"all": "ALL ", "regex": "REG ", "root_zone_db": "RZD "}

    # List all links we are going to call/use.
    LINKS = {
        "core": "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/whitelist/master/domains.list",  # pylint: disable=line-too-long
        "root_zone_db": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/iana-domains-db.json",  # pylint: disable=line-too-long
        "public_suffix": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/public-suffix.json",  # pylint: disable=line-too-long
    }

    def __init__(
        self,
        file=None,
        string=None,
        items=None,
        output_file=None,
        secondary_whitelist_file=None,
        use_core=True,
    ):  # pylint: disable=too-many-arguments
        self.secondary_whitelist_file = secondary_whitelist_file
        self.file = file
        self.string = string
        self.items = items
        self.output = output_file
        self.use_core = use_core

        self.regex_rz_db = RZDB().regex_format()

    def __parse_whitelist_list(self, line):
        """
        Parse the whiteslist list into something the system understand.

        :param line: The whitelist line.
        :type line: str

        :return: The great formatted whitelisst elemetn
        :rtype: str
        """

        if line and not line.startswith("#"):
            if line.startswith(self.MAKERS["all"]):
                whitelist_element = "{}$".format(
                    escape(line.split(self.MAKERS["all"])[-1].strip())
                )
            elif line.startswith(self.MAKERS["regex"]):
                whitelist_element = "{}".format(
                    line.split(self.MAKERS["regex"])[-1].strip()
                )
            elif line.startswith(self.MAKERS["root_zone_db"]):
                to_check = line.split(self.MAKERS["root_zone_db"])[-1].strip()

                if to_check.endswith("."):
                    to_check = to_check[:-1]

                to_check = escape(to_check)

                if not to_check.startswith("www."):
                    whitelist_element = [
                        "^{}{}$".format(to_check, self.regex_rz_db),
                        "^www.{}{}$".format(to_check, self.regex_rz_db),
                    ]
                else:
                    whitelist_element = [
                        "^{}{}$".format(to_check, self.regex_rz_db),
                        "^{}{}$".format(
                            ".".join(to_check.split(".")[1:]), self.regex_rz_db
                        ),
                    ]
            else:
                to_check = escape(line.strip())

                if not to_check.startswith("www."):
                    whitelist_element = [
                        "^{}$".format(to_check),
                        "^www.{}$".format(to_check),
                    ]
                else:
                    whitelist_element = [
                        "^{}$".format(to_check),
                        "^{}$".format(".".join(to_check.split(".")[1:])),
                    ]

            yield whitelist_element

    def __get_whitelist_list(self):
        """
        Get whitelist list.

        :return: The whitelist in list and regex format.
        :rtype: tuple
        """

        whiteslist_list = []

        if self.use_core:
            data = Download(self.LINKS["core"], destination=None).link().split("\n")
        else:
            data = []

        if self.secondary_whitelist_file and isinstance(
            self.secondary_whitelist_file, list
        ):
            for file in self.secondary_whitelist_file:
                data.extend(file.read().splitlines())

        if data:
            for element in [
                self.__parse_whitelist_list(x) for x in List(data).format()
            ]:
                for content in element:
                    if isinstance(content, list):
                        whiteslist_list.extend(content)
                    else:
                        whiteslist_list.append(content)

        whiteslist_list.append(
            r"((192)\.(168)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))|((10)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))|((172)\.(1[6-9]|2[0-9]|3[0-1])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))"  # pylint: disable=line-too-long
        )

        return whiteslist_list, "|".join(whiteslist_list)

    @classmethod
    def __format_upstream_line(cls, line):  # pylint: disable=too-many-branches
        """
        Format the given line in order to only extract the domain.

        :param line: The line to format.
        :type line: str
        """

        if line.startswith("#"):
            return line

        regex_delete = r"localhost$|localdomain$|local$|broadcasthost$|0\.0\.0\.0$|allhosts$|allnodes$|allrouters$|localnet$|loopback$|mcastprefix$"  # pylint: disable=line-too-long
        comment = ""
        element = ""
        tabs = "\t"
        space = " "

        if Regex(line, regex_delete, return_data=True).match():
            return line

        tabs_position, space_position = (line.find(tabs), line.find(space))

        if tabs_position > -1 and space_position > -1:
            if space_position < tabs_position:
                separator = space
            else:
                separator = tabs
        elif not tabs_position == -1:
            separator = tabs
        elif not space_position == -1:
            separator = space
        else:
            separator = None

        if separator:
            splited_line = line.split(separator)

            index = 0
            while index < len(splited_line):
                if (
                    splited_line[index]
                    and not Regex(
                        splited_line[index], regex_delete, return_data=False
                    ).match()
                ):
                    break
                index += 1

            if "#" in splited_line[index]:
                index_comment = splited_line[index].find("#")

                if index_comment > -1:
                    comment = splited_line[index][index_comment:]

                    element = splited_line[index].split(comment)[0]
                    splited_line[index] = domain2idna(element) + comment

            return separator.join(splited_line)
        return domain2idna(line)

    def __write_output(self, line):
        """
        Write the output file.

        :param line: One or multiple lines.
        :type line: str or list

        :return: The lines
        """

        if self.output:
            if isinstance(line, list):
                line = "\n".join(line)

            File(self.output).write("{}\n".format(line), overwrite=False)

        return line

    def filter(self):
        """
        Process the whitelisting.
        """

        content = []
        _, regex_whitelist = self.__get_whitelist_list()

        if self.file:
            content.extend(
                [self.__format_upstream_line(x) for x in File(self.file).to_list()]
            )
        elif self.string:
            content.extend(
                [self.__format_upstream_line(x) for x in self.string.split("\n")]
            )
        elif self.items:
            content.extend([self.__format_upstream_line(x) for x in self.items])

        if content and regex_whitelist:
            if self.output:
                File(self.output).write("", overwrite=True)

            return self.__write_output(
                Regex(content, regex_whitelist, return_data=False).not_matching_list()
            )

        return content


class RZDB:
    """
    Extract and manipulate the RZDB.
    """

    @classmethod
    def __get_database(cls):
        """
        Get a copy of the Root zone database.
        """

        return [
            x
            for x in loads(
                Download(Core.LINKS["root_zone_db"], destination=None).link()
            ).keys()
        ]

    @classmethod
    def __get_public_suffix(cls):
        """
        Get a copy of the public suffix database.
        """

        return [
            suffix
            for suffixes in loads(
                Download(Core.LINKS["public_suffix"], destination=None).link()
            ).values()
            for suffix in suffixes
        ]

    def list_format(self):
        """
        Return the list format.
        """

        result = self.__get_database()
        result.extend(self.__get_public_suffix())

        return List(result).format()

    def regex_format(self):
        """
        Return the regex format.
        """

        return r"((?:\.(?:{})))".format(
            "|".join([escape(x) for x in self.list_format()])
        )
