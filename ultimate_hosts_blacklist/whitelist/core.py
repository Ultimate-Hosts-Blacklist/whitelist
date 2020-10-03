"""
The whitelisting tool from the Ultimate-Hosts-Blacklist project.

Provide the main logic.

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


import logging
import sys
from itertools import filterfalse
from multiprocessing import Pool
from os import cpu_count, environ, sep
from tempfile import NamedTemporaryFile, TemporaryDirectory

import PyFunceble
from domain2idna import domain2idna

from ultimate_hosts_blacklist.helpers import Download, File, Regex
from ultimate_hosts_blacklist.whitelist.configuration import Configuration
from ultimate_hosts_blacklist.whitelist.parser import Parser


def _is_whitelisted(line, manifest):  # pylint: disable=too-many-branches
    """
    Check if the given line is whitelisted.
    """

    if not line:
        logging.debug("Empty line whitelisted by default.")
        return True, line

    if isinstance(line, bytes):  # pragma: no cover
        line = line.decode()

    logging.debug("Given line: %s", repr(line))
    line = line.strip()

    if isinstance(line, str):
        to_check = line.split()[-1]

        try:
            url_base = PyFunceble.Check(to_check).is_url(return_base=True)
        except AttributeError:  # pragma: no cover
            PyFunceble.load_config(generate_directory_structure=False)
            url_base = PyFunceble.Check(to_check).is_url(return_base=True)

        if url_base is not False:  # pragma: no cover
            to_check = url_base
    else:  # pragma: no cover
        raise ValueError("expected {0}. {1} given.".format(str, type(line)))

    logging.debug("To check: %s", repr(to_check))

    if manifest:
        if to_check.startswith("www."):
            bare = to_check[4:]
        else:
            bare = to_check

        if bare[:4] in manifest["strict"] and to_check in manifest["strict"][bare[:4]]:
            logging.debug(
                "Line %s whitelisted by %s rule: %s.",
                repr(line),
                repr("strict"),
                repr(line),
            )
            return True, line

        if (
            bare[:4] in manifest["present"]
            and to_check in manifest["present"][bare[:4]]
        ):
            logging.debug(
                "Line %s whitelisted by %s rule.", repr(line), repr("present")
            )
            return True, line

        if bare[-3:] in manifest["ends"]:  # pragma: no cover
            for rule in manifest["ends"][bare[-3:]]:
                if to_check.endswith(rule):
                    logging.debug(
                        "Line %s whitelisted by %s rule: %s.",
                        repr(line),
                        repr("ends"),
                        repr(rule),
                    )
                    return True, line

        if (
            manifest["regex"]
            and Regex(to_check, manifest["regex"], return_data=False).match()
        ):
            logging.debug("Line %s whitelisted by %s rule.", repr(line), repr("regex"))
            return True, line

    logging.debug("Line %s not whitelisted, no rule matched.", repr(line))
    return False, line


class Core:  # pylint: disable=too-few-public-methods,too-many-arguments, too-many-instance-attributes
    """
    Brain of our system.

    :param str output_file:
        The path to the file to write.
    :param list secondary_whitelist:
        A whitelist list to parse.
    :param str secondary_whitelist_file:
        A path to a whitelist file to parse.
    :param list anti_whitelist:
        A list of whitelist rule to exclude.
    :param str anti_whitelist_file:
        A path to a whitelit file containing the
        rule we have to exclude.
    :param bool use_official:
        Allows us to download and use the official
        whitelist list of the ultimate hosts blacklist project.
    :param bool multiprocessing:
        Allows us to use more than one process for the
        whitelisting process.
    :param int processes:
        The number of processes we are allowed to use.

        .. note::
            If equal to :code:`0`, we use :code:`os.cpu_count() // 2`.
    :param int logging_level:
        The minimum logging level.
    :param bool logging_into_file:
        Allows us to log into a file called :code:`uhb_whitelist_debug`.
    :param bool no_complement:
        Forbid us the generation of complements while parsing the
        whitelist list.

        Complements are `www.example.org` if `example.org` is given and vice-versa.
    :param list all_whitelist:
        A whitelist list to prefix "ALL " and parse.
    :param str all_whitelist_file:
        A path to a whitelist file,
        to prefix "ALL " and parse.
    :param list reg_whitelist:
        A whitelist list to prefix "REG " and parse.
    :param str reg_whitelist_file:
        A path to a whitelist file,
        to prefix "REG " and parse.
    :param list rzd_whitelist:
        A whitelist list to prefix "RZD " and parse.
    :param str rzd_whitelist_file:
        A path to a whitelist file,
        to prefix "RZD " and parse.
    """

    # pylint: disable=too-many-locals

    files_to_delete = []

    def __init__(
        self,
        output_file=None,
        secondary_whitelist=None,
        secondary_whitelist_file=None,
        anti_whitelist=None,
        anti_whitelist_file=None,
        use_official=True,
        multiprocessing=True,
        processes=0,
        logging_level=logging.INFO,
        logging_into_file=False,
        no_complement=False,
        all_whitelist=None,
        all_whitelist_file=None,
        reg_whitelist=None,
        reg_whitelist_file=None,
        rzd_whitelist=None,
        rzd_whitelist_file=None,
    ):

        if logging_into_file:  # pragma: no cover
            logging_file = "uhb_whitelist_debug"
        else:
            logging_file = None

        logging.basicConfig(
            format="%(asctime)s - %(levelname)s -- %(message)s",
            level=logging_level,
            filename=logging_file,
        )

        self.pyfunceble_config_dir = TemporaryDirectory(prefix="UHBW_PYFUNCEBLE")
        environ["PYFUNCEBLE_AUTO_CONFIGURATION"] = "YES"
        PyFunceble.CONFIG_DIRECTORY = self.pyfunceble_config_dir.name + sep

        PyFunceble.load_config(generate_directory_structure=False)

        self.temporary_output_file = self.__get_temp_file().name

        self.secondary_whitelist_file = self.__download_file(secondary_whitelist_file)
        self.secondary_whitelist_list = secondary_whitelist
        self.anti_whitelist_list = anti_whitelist
        self.anti_whitelist_file = self.__download_file(anti_whitelist_file)

        self.all_whitelist_list = all_whitelist
        self.all_whitelist_file = self.__download_file(all_whitelist_file)
        self.reg_whitelist_list = reg_whitelist
        self.reg_whitelist_file = self.__download_file(reg_whitelist_file)
        self.rzd_whitelist_list = rzd_whitelist
        self.rzd_whitelist_file = self.__download_file(rzd_whitelist_file)

        self.output = output_file
        self.use_core = use_official

        parser = Parser(no_complement=no_complement)
        self.whitelist_process = parser.parse(self.__get_whitelist_list_to_parse())

        self.multiprocessing = multiprocessing

        if self.multiprocessing:
            if not processes:
                self.processes = cpu_count() // 2
            else:
                self.processes = processes

    def __del__(self):
        if self.output:
            PyFunceble.helpers.File(self.temporary_output_file).move(self.output)

        for file_path in self.files_to_delete:
            PyFunceble.helpers.File(file_path=file_path).delete()

        self.pyfunceble_config_dir.cleanup()

    @classmethod
    def __get_our_special_rules(cls):
        """
        Return some special rules which should be always added to the system.
        """

        return [
            # Match 0.0.0.0–0.255.255.255
            r"REG ^(0\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 10.0.0.0–10.255.255.255
            r"REG ^(10\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 100.64.0.0–100.127.255.255
            r"REG ^(100\.(0?6[4-9]|0?[7-9][0-9]|1[0-1][0-9]|12[0-7])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 127.0.0.0–127.255.255.255
            r"REG ^(127\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 169.254.0.0–169.254.255.255
            r"REG ^(169\.254\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 172.16.0.0–172.31.255.255
            r"REG ^(172\.(0?1[6-9]|0?2[0-9]|0?3[0-1])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 192.0.0.0–192.0.0.255
            r"REG ^(192\.0\.0\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 192.0.2.0–192.0.2.255
            r"REG ^(192\.0\.2\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 192.88.99.0–192.88.99.255
            r"REG ^(192\.88\.99\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 192.168.0.0–192.168.255.255
            r"REG ^(192\.168\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 198.18.0.0–198.19.255.255
            r"REG ^(198\.(0?1[8-9])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 198.51.100.0–198.51.100.255
            r"REG ^(198\.51\.100\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 203.0.113.0–203.0.113.255
            r"REG ^(203\.0\.113\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))$",  # pylint: disable=line-too-long
            # Match 224.0.0.0–239.255.255.255
            r"REG ^(22[4-9]|23[0-9])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,})$",  # pylint: disable=line-too-long
            # Match 240.0.0.0–255.255.255.254
            r"REG ^(24[0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,})$",  # pylint: disable=line-too-long
            # Match 255.255.255.255
            r"255.255.255.255",  # pylint: disable=line-too-long
        ]

    @classmethod
    def __get_file_obj_from_path(cls, file, force_check=True):  # pragma: no cover
        """
        Provides a file object of the given :code:`file`
        if it exists.
        """

        if force_check and file is not None:
            if not PyFunceble.helpers.File(file).exists():
                print(f"Error: {file} does not exist.")
                sys.exit(1)

            return open(file, "r")

        return file

    def __get_temp_file(self):  # pragma: no cover
        """
        Provides a new temporary file.
        """

        destination = NamedTemporaryFile(delete=False)
        self.files_to_delete.append(destination.name)

        return destination

    def __download_file(self, file):  # pragma: no cover
        """
        Downloads the given file if it's a URL and return
        the new file destination.
        """

        if isinstance(file, list):
            return [self.__download_file(x) for x in file]

        if file:
            if PyFunceble.Check(file).is_url():
                destination = self.__get_temp_file()
                PyFunceble.helpers.Download(file).text(destination=destination.name)

                return destination

            return self.__get_file_obj_from_path(file)
        return file

    def __get_secondary_whitelist_rules(self):
        """
        Provides the rules which are into the
        secondary whitelist lists.
        """

        result = []

        if self.secondary_whitelist_file and isinstance(
            self.secondary_whitelist_file, list
        ):  # pragma: no cover
            for file in self.secondary_whitelist_file:
                result.extend(file.read().splitlines())

        if self.secondary_whitelist_list and isinstance(
            self.secondary_whitelist_list, list
        ):
            result.extend(self.secondary_whitelist_list)

        return result

    def __apply_anti_whitelist_rules(self, rules):
        """
        Provides the rules anti whitelists rules.
        """

        result = rules

        if self.anti_whitelist_file and isinstance(
            self.anti_whitelist_file, list
        ):  # pragma: no cover

            anti_content = []

            for anti_file in self.anti_whitelist_file:
                anti_content.extend(anti_file.read().splitlines())

            result = list(set(result) - set(anti_content))

        if self.anti_whitelist_list and isinstance(self.anti_whitelist_list, list):
            result = list(set(result) - set(self.anti_whitelist_list))

        return result

    def __get_all_prefixed_whitelist_rules(self):  # pragma: no cover
        """
        Provides the rules which are into the
        ALL whitelist lists.

        .. warning::
            This method automatically appends the marker.
        """

        result = []

        if self.all_whitelist_file and isinstance(self.all_whitelist_file, list):
            for file in self.all_whitelist_file:
                result.extend(
                    [
                        f'{Configuration.markers["all"]}{x}'
                        for x in file.read().splitlines()
                    ]
                )

        if self.all_whitelist_list and isinstance(self.all_whitelist_list):
            result.extend(
                [f'{Configuration.markers["all"]}{x}' for x in self.all_whitelist_list]
            )

        return result

    def __get_reg_prefixed_whitelist_rules(self):  # pragma: no cover
        """
        Provides the rules which are into the
        REG whitelist lists.

        .. warning::
            This method automatically appends the marker.
        """

        result = []

        if self.reg_whitelist_file and isinstance(self.reg_whitelist_file, list):
            for file in self.reg_whitelist_file:
                result.extend(
                    [
                        f'{Configuration.markers["regex"]}{x}'
                        for x in file.read().splitlines()
                    ]
                )

        if self.reg_whitelist_list and isinstance(self.reg_whitelist_list):
            result.extend(
                [f'{Configuration.markers["all"]}{x}' for x in self.reg_whitelist_list]
            )

        return result

    def __get_rzd_prefixed_whitelist_rules(self):  # pragma: no cover
        """
        Provides the rules which are into the
        RZD whitelist lists.

        .. warning::
            This method automatically appends the marker.
        """

        result = []

        if self.rzd_whitelist_file and isinstance(self.rzd_whitelist_file, list):
            for file in self.rzd_whitelist_file:
                result.extend(
                    [
                        f'{Configuration.markers["root_zone_db"]}{x}'
                        for x in file.read().splitlines()
                    ]
                )

        if self.rzd_whitelist_list and isinstance(self.rzd_whitelist_list):
            result.extend(
                [
                    f'{Configuration.markers["root_zone_db"]}{x}'
                    for x in self.rzd_whitelist_list
                ]
            )

        return result

    def __get_whitelist_list_to_parse(self):
        """
        Return the not parsed/formatted whitelist list.
        """

        if self.use_core:
            result = (
                Download(Configuration.links["core"], destination=None)
                .link()
                .split("\n")
            )
        else:
            result = []

        result.extend(self.__get_our_special_rules())
        result.extend(self.__get_secondary_whitelist_rules())

        result.extend(self.__get_all_prefixed_whitelist_rules())
        result.extend(self.__get_reg_prefixed_whitelist_rules())
        result.extend(self.__get_rzd_prefixed_whitelist_rules())

        return self.__apply_anti_whitelist_rules(result)

    @classmethod
    def format_upstream_line(cls, line):  # pylint: disable=too-many-branches
        """
        Format the given line in order to habe the domain in IDNA format.

        :param line: The line to format.
        :type line: str
        """

        if isinstance(line, bytes):
            line = line.decode()

        if not line or line.startswith("#"):
            return line

        regex_delete = r"localhost$|localdomain$|local$|broadcasthost$|0\.0\.0\.0$|allhosts$|allnodes$|allrouters$|localnet$|loopback$|mcastprefix$"  # pylint: disable=line-too-long
        comment = ""
        element = ""
        tabs = "\t"
        space = " "

        if Regex(line, regex_delete, return_data=True).match():  # pragma: no cover
            return line

        tabs_position, space_position = (line.find(tabs), line.find(space))

        if not tabs_position == -1:
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
            else:
                splited_line[index] = domain2idna(splited_line[index])

            return separator.join(splited_line)
        return domain2idna(line)

    def __write_output(
        self, line, standard_sorting, hierarchical_sorting
    ):  # pragma: no cover
        """
        Write the output file.

        :param line: One or multiple lines.
        :type line: str or list

        :return: The lines
        """

        line = [x.strip() for x in line if x.strip()]

        if self.output:
            if isinstance(line, list):
                line = "\n".join(
                    self.__process_sorting(line, standard_sorting, hierarchical_sorting)
                )

            File(self.temporary_output_file).write("{0}\n".format(line), overwrite=True)

        return line

    def _get_content(
        self, input_file=None, string=None, items=None, already_formatted=False
    ):  # pragma: no cover
        """
        Return the content we have to check.
        """

        result = []

        input_file = self.__get_file_obj_from_path(input_file)

        if input_file:
            result.extend(input_file.read().splitlines())
        if string:
            if not already_formatted:
                for line in string.split("\n"):
                    result.append(self.format_upstream_line(line))
            else:
                result.extend(string.split("\n"))

        if items:
            if not already_formatted:
                for line in items:
                    result.append(self.format_upstream_line(line))
            else:
                result.extend(items)

        del input_file, items, string

        return result

    @classmethod
    def __process_sorting(cls, to_sort, standard, hierarchical):  # pragma: no cover
        """
        Process the sorting of the list.
        """

        if standard:
            return PyFunceble.helpers.List(to_sort).custom_format(
                PyFunceble.engine.Sort.standard
            )

        if hierarchical:
            return PyFunceble.helpers.List(to_sort).custom_format(
                PyFunceble.engine.Sort.hierarchical
            )

        return to_sort

    def filter(
        self,
        file=None,
        string=None,
        items=None,
        already_formatted=False,
        standard_sort=False,
        hierarchical_sort=False,
    ):
        """
        Process the whitelisting.
        """

        if self.whitelist_process:

            if self.multiprocessing:
                result = []

                with Pool(processes=self.processes) as pool:
                    for whitelisted, line in pool.starmap(
                        _is_whitelisted,
                        [
                            [x, self.whitelist_process]
                            for x in self._get_content(
                                input_file=file,
                                string=string,
                                items=items,
                                already_formatted=already_formatted,
                            )
                        ],
                    ):
                        if whitelisted is False:
                            result.append(line)

                return self.__write_output(result, standard_sort, hierarchical_sort)

            return self.__write_output(
                list(
                    filterfalse(
                        lambda x: _is_whitelisted(x, self.whitelist_process)[0] is True,
                        self._get_content(
                            input_file=file,
                            string=string,
                            items=items,
                            already_formatted=already_formatted,
                        ),
                    )
                ),
                standard_sort,
                hierarchical_sort,
            )

        return self.__write_output(
            self._get_content(
                input_file=file,
                string=string,
                items=items,
                already_formatted=already_formatted,
            ),
            standard_sort,
            hierarchical_sort,
        )  # pragma: no cover
