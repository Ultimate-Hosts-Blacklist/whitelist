"""
The whitelist script of the Ultimate-Hosts-Blacklist project.

Provide the helpers

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
# pylint: disable=bad-continuation

from os import path
from re import compile as comp

from requests import get


class List:  # pylint: disable=too-few-public-methods
    """
    List manipulation.
    """

    def __init__(self, main_list=None):
        if main_list is None:  # pragma: no cover
            self.main_list = []
        else:
            self.main_list = main_list

    def format(self):
        """
        Return a well formated list. Basicaly, it's sort a list and remove duplicate.
        """

        try:
            return sorted(list(set(self.main_list)), key=str.lower)
        except TypeError:  # pragma: no cover
            return self.main_list


class File:  # pylint: disable=too-few-public-methods  # pragma: no cover
    """
    File treatment/manipulations.

    Argument:
        - file: str
            - a path to the file to manipulate.
    """

    def __init__(self, file):
        self.file = file

    def read(self):
        """
        Read a given file path and return its content.
        """

        with open(self.file, "r", encoding="utf-8") as file:
            funilrys = file.read()

        return funilrys

    def to_list(self):
        """
        Read a file path and return each line as a list element.
        """

        result = []

        with open(self.file, "r", encoding="utf-8") as file:
            result = file.read().splitlines()

        return result

    def write(self, data_to_write, overwrite=False):
        """
        Write or append data into the given file path.

        Argument:
            - data_to_write: str
                The data to write.
        """

        if data_to_write is not None and isinstance(data_to_write, str):
            if overwrite or not path.isfile(self.file):
                with open(self.file, "w", encoding="utf-8") as file:
                    file.write(data_to_write)
            else:
                with open(self.file, "a", encoding="utf-8") as file:
                    file.write(data_to_write)


class Download:  # pylint: disable=too-few-public-methods  # pragma: no cover
    """
    This class will initiate a download of the desired link.

    Arguments:
        - link_to_download: str
            The link to the file we are going to download.
        - destination: str
            The destination of the downloaded data.
    """

    def __init__(self, link_to_download, destination, convert_to_idna=False):
        self.link_to_download = link_to_download
        self.destination = destination
        self.convert_to_idna = convert_to_idna

    def _convert_to_idna(self, data):
        """
        This method convert a given data into IDNA format.

        Argument:
            - data: str
                The downloaded data.
        """

        if self.convert_to_idna:
            to_write = []

            for line in data.split("\n"):
                line = line.split()
                try:
                    if isinstance(line, list):
                        converted = []
                        for string in line:
                            converted.append(string.encode("idna").decode("utf-8"))

                        to_write.append(" ".join(converted))
                    else:
                        to_write.append(line.encode("idna").decode("utf-8"))
                except UnicodeError:
                    if isinstance(line, list):
                        to_write.append(" ".join(line))
                    else:
                        to_write.append(line)
            return to_write

        return None

    def link(self):
        """
        This method initiate the download.
        """

        if self.link_to_download:
            request = get(self.link_to_download)

            if request.status_code == 200:
                if self.destination:
                    if self.convert_to_idna:
                        File(self.destination).write(
                            "\n".join(self._convert_to_idna(request.text)),
                            overwrite=True,
                        )
                    else:
                        File(self.destination).write(request.text, overwrite=True)
                else:
                    return request.text

                del request

                return True

        return False


class Regex:  # pylint: disable=too-few-public-methods

    """A simple implementation ot the python.re package

    Arguments:
        - data: str
            The data to regex check.
        - regex: str
            The regex to match.
        - group: int
            The group to return
        - replace_with: str
            The value to replace the matched regex with.
        - occurences: int
            The number of occurence(s) to replace.
    """

    def __init__(self, data, regex, **args):
        # We initiate the needed variable in order to be usable all over
        # class
        self.data = data

        # We assign the default value of our optional arguments
        optional_arguments = {
            "escape": False,
            "group": 0,
            "occurences": 0,
            "return_data": True,
        }

        # We initiate our optional_arguments in order to be usable all over the
        # class
        for (arg, default) in optional_arguments.items():
            setattr(self, arg, args.get(arg, default))

            self.regex = regex

    def match(self):
        """
        Used to get exploitable result of re.search
        """

        # We compile the regex string
        to_match = comp(self.regex)

        # In case we have to use the implementation of ${BASH_REMATCH} we use
        # re.findall otherwise, we use re.search
        pre_result = to_match.search(self.data)

        if self.return_data and pre_result:  # pylint: disable=no-member
            return pre_result.group(self.group).strip()  # pylint: disable=no-member

        if not self.return_data and pre_result:  # pylint: disable=no-member
            return True

        return False

    def not_matching_list(self):
        """
        This method return a list of string which don't match the
        given regex.
        """

        pre_result = comp(self.regex)

        return list(
            filter(lambda element: not pre_result.search(str(element)), self.data)
        )
