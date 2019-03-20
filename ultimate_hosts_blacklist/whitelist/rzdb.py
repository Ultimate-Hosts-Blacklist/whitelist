"""
The whitelist script of the Ultimate-Hosts-Blacklist project.

Provide the Root Zone DataBase (RZDB).

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

from json import loads
from re import escape

from ultimate_hosts_blacklist.helpers import Download, List
from ultimate_hosts_blacklist.whitelist.configuration import Configuration


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
                Download(Configuration.links["root_zone_db"], destination=None).link()
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
                Download(Configuration.links["public_suffix"], destination=None).link()
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

    def regex_format(self):  # pragma: no cover
        """
        Return the regex format.
        """

        return r"((?:\.(?:{0})))".format(
            "|".join([escape(x) for x in self.list_format()])
        )
