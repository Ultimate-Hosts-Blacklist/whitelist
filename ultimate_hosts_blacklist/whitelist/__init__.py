"""
The whitelisting tool from the Ultimate-Hosts-Blacklist project.

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
import argparse
from logging import DEBUG, INFO
from os import environ
from tempfile import gettempdir

from colorama import Fore, Style
from colorama import init as initiate

from ultimate_hosts_blacklist.whitelist.core import Core

VERSION = "3.25.0"

environ["PYFUNCEBLE_CONFIG_DIR"] = gettempdir()
environ["PYFUNCEBLE_AUTO_CONFIGURATION"] = "YES"


def clean_string_with_official_whitelist(
    data,
    use_official=True,
    your_whitelist_list=None,
    your_anti_whitelist_list=None,
    multiprocessing=False,
    processes=0,
    no_complement=False,
    your_all_list=None,
    your_reg_list=None,
    your_rzd_list=None,
):  # pylint: disable=too-many-arguments
    """
    Clean the given string.

    .. note:
        We consider 1 element per line.

    :param str data: The string to clean.
    :pram bool use_official: Allow us to use your official whitelist list.
    :param list your_whitelist_list:
        Your whitelist list.

        .. note::
            It should follow our format.

    :param list your_anti_whitelist_list:
        Your anti whitelist list.
        Basically a list of rule which we don't have to follow.

        .. note::
            It should follow our format.

    :param bool multiprocessing: Tell us to use more than one process.

    :param int processes:
        The number of processes to use.

        .. note::
            If equal to :code:`0`, we use :code:`os.cpu_count() // 2`.

    :param bool no_complement:
        Forbid us the generation of complements while parsing the
        whitelist list.

        Complements are `www.example.org` if `example.org` is given and vice-versa.

    :param list your_all_list:
        Your list of subject to whitelisst.
        Basically a list which we prefix "ALL " to.

        .. note::
            It should follow our format.

    :param list your_reg_list:
        Your list of subject to whitelisst.
        Basically a list which we prefix "REG " to.

        .. note::
            It should follow our format.

    :param list your_rzd_list:
        Your list of subject to whitelisst.
        Basically a list which we prefix "RZD " to.

        .. note::
            It should follow our format.

    :return: A string without the whitelisted elements.
    :rtype: string
    """

    return "\n".join(
        Core(
            use_official=use_official,
            secondary_whitelist=your_whitelist_list,
            anti_whitelist=your_anti_whitelist_list,
            multiprocessing=multiprocessing,
            processes=processes,
            no_complement=no_complement,
            all_whitelist=your_all_list,
            reg_whitelist=your_reg_list,
            rzd_whitelist=your_rzd_list,
        ).filter(string=data)
    )


def clean_list_with_official_whitelist(
    data,
    use_official=True,
    your_whitelist_list=None,
    your_anti_whitelist_list=None,
    multiprocessing=False,
    processes=0,
    no_complement=False,
    your_all_list=None,
    your_reg_list=None,
    your_rzd_list=None,
):  # pylint: disable=too-many-arguments
    """
    Clean the given list.

    :param list data: The list to clean.

    :param str data: The string to clean.

    :pram bool use_core: Allow us to use your official whitelist list.

    :param list your_whitelist_list:
        Your whitelist list.

        .. note::
            It should follow our format.

     :param list your_anty_whitelist_list:
        Your anti whitelist list.
        Basically a list of rule which we don't have to follow.

        .. note::
            It should follow our format.

    :param bool multiprocessing: Tell us to use more than one process.

    :param int processes:
        The number of processes to use.

        .. note::
            If equal to :code:`0`, we use :code:`os.cpu_count() // 2`.

    :param bool no_complement:
        Forbid us the generation of complements while parsing the
        whitelist list.

        Complements are `www.example.org` if `example.org` is given and vice-versa.

    :param list your_all_list:
        Your list of subject to whitelisst.
        Basically a list which we prefix "ALL " to.

        .. note::
            It should follow our format.

    :param list your_reg_list:
        Your list of subject to whitelisst.
        Basically a list which we prefix "REG " to.

        .. note::
            It should follow our format.

    :param list your_rzd_list:
        Your list of subject to whitelisst.
        Basically a list which we prefix "RZD " to.

        .. note::
            It should follow our format.

    :return: A list without the whitelisted elements.
    :rtype: list
    """

    return Core(
        use_official=use_official,
        secondary_whitelist=your_whitelist_list,
        anti_whitelist=your_anti_whitelist_list,
        multiprocessing=multiprocessing,
        processes=processes,
        no_complement=no_complement,
        all_whitelist=your_all_list,
        reg_whitelist=your_reg_list,
        rzd_whitelist=your_rzd_list,
    ).filter(items=data)


def _command_line():
    """
    Provide the CLI.
    """

    # We initiate the auto coloration
    initiate(autoreset=True)

    parser = argparse.ArgumentParser(
        description="UHBW is a tool to clean up lists or hosts files with the "
        "hosted and/or your own whitelist.",
        epilog="Crafted with %s by %s"
        % (
            Fore.RED + "♥" + Fore.RESET,
            Style.BRIGHT + Fore.YELLOW + "Nissar Chababy (Funilrys) " + Style.RESET_ALL,
        ),
    )

    parser.add_argument(
        "-a",
        "--anti-whitelist",
        type=str,
        nargs="+",
        help="Read the given file override rules from the UHBW hosted "
        "whitelist which is used by default. (See also `-wc`)",
    )

    parser.add_argument(
        "--all",
        type=str,
        nargs="+",
        help="Read the given file(s) and append its rules to the whitelisting schema. "
        f"{Fore.GREEN}{Style.BRIGHT}Note: The rules injected through this argument "
        f"will be automatically prefixed with the `ALL` marker.{Style.RESET_ALL}",
    )

    parser.add_argument(
        "-d",
        "--debug",
        help="Activate the debug mode. This mode will write the whole "
        "processes to stdout.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-df",
        "--debug-into-file",
        help="Activate the logging into a file called `uhb_whitelist_debug` "
        "at the current location.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="The file to whitelist/clean.",
    )

    parser.add_argument(
        "--hierachical-sorting",
        action="store_true",
        default=False,
        help="Process a hierarchical sorting when outputing into a file.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Save the result to the given filename or path. (Can not "
        "be the same as input file `-f`)",
    )

    parser.add_argument(
        "-m",
        "--multiprocessing",
        action="store_true",
        default=False,
        help="Activate the usage of multiple core processes.",
    )

    parser.add_argument(
        "--no-complement",
        action="store_true",
        default=False,
        help="Forbid us the generation of complements while parsing the "
        "whitelist list. Complements are `www.example.org` if "
        "`example.org` is given and vice-versa.",
    )

    parser.add_argument(
        "-p",
        "--processes",
        type=int,
        default=0,
        help="The number of (maximal) processes core to use.",
    )

    parser.add_argument(
        "--reg",
        type=str,
        nargs="+",
        help="Read the given file(s) and append its rules to the whitelisting schema. "
        f"{Fore.GREEN}{Style.BRIGHT}Note: The rules injected through this argument "
        f"will be automatically prefixed with the `REG` marker.{Style.RESET_ALL}",
    )

    parser.add_argument(
        "--rzd",
        type=str,
        nargs="+",
        help="Read the given file(s) and append its rules to the whitelisting schema. "
        f"{Fore.GREEN}{Style.BRIGHT}Note: The rules injected through this argument "
        f"will be automatically prefixed with the `RZD` marker.{Style.RESET_ALL}",
    )

    parser.add_argument(
        "--standard-sorting",
        action="store_true",
        default=False,
        help="Process a sorting when outputing into a file.",
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Show the version end exist.",
        action="version",
        version="%(prog)s " + VERSION,
    )

    parser.add_argument(
        "-w",
        "--whitelist",
        type=str,
        nargs="+",
        help="Read the given file(s) and append its rules to the whitelisting schema. "
        f"{Fore.GREEN}{Style.BRIGHT}Note: The rules injected through this argument "
        "won't be changed. We follow what you give us. That means that if you "
        "give any of our supported rules, they will still be appended to the "
        f"whitelisting schema.{Style.RESET_ALL}",
    )

    parser.add_argument(
        "-wc",
        "--without-core",
        action="store_false",
        help="Disable the usage of the Ultimate Hosts Blacklist "
        "whitelist hosted list.",
    )

    arguments = parser.parse_args()

    if arguments.debug:
        logging_level = DEBUG
    else:
        logging_level = INFO

    if arguments.file:
        if not arguments.output:
            print(
                "\n".join(
                    Core(
                        secondary_whitelist_file=arguments.whitelist,
                        anti_whitelist_file=arguments.anti_whitelist,
                        use_official=arguments.without_core,
                        multiprocessing=arguments.multiprocessing,
                        processes=arguments.processes,
                        logging_level=logging_level,
                        logging_into_file=arguments.debug_into_file,
                        no_complement=arguments.no_complement,
                        all_whitelist_file=arguments.all,
                        reg_whitelist_file=arguments.reg,
                        rzd_whitelist_file=arguments.rzd,
                    ).filter(
                        file=arguments.file,
                        standard_sort=arguments.standard_sorting,
                        hierarchical_sort=arguments.hierachical_sorting,
                    )
                )
            )
        else:
            Core(
                secondary_whitelist_file=arguments.whitelist,
                anti_whitelist_file=arguments.anti_whitelist,
                output_file=arguments.output,
                use_official=arguments.without_core,
                multiprocessing=arguments.multiprocessing,
                processes=arguments.processes,
                logging_level=logging_level,
                logging_into_file=arguments.debug_into_file,
                no_complement=arguments.no_complement,
                all_whitelist_file=arguments.all,
                reg_whitelist_file=arguments.reg,
                rzd_whitelist_file=arguments.rzd,
            ).filter(
                file=arguments.file,
                standard_sort=arguments.standard_sorting,
                hierarchical_sort=arguments.hierachical_sorting,
            )
