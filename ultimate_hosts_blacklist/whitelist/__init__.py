"""
The whitelisting tool from the Ultimate-Hosts-Blacklist project.

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
# pylint: disable=bad-continuation
import argparse
from logging import DEBUG, INFO
from os import environ
from tempfile import gettempdir

from colorama import Fore, Style
from colorama import init as initiate

from ultimate_hosts_blacklist.helpers import File
from ultimate_hosts_blacklist.whitelist.core import Core

VERSION = "3.18.0"

environ["PYFUNCEBLE_CONFIG_DIR"] = gettempdir()
environ["PYFUNCEBLE_AUTO_CONFIGURATION"] = "TRUE"


def clean_string_with_official_whitelist(
    data,
    use_official=True,
    your_whitelist_list=None,
    your_anti_whitelist_list=None,
    multiprocessing=False,
    processes=0,
    no_complement=False,
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
    ).filter(items=data)


def _command_line():
    """
    Provide the CLI.
    """

    # We initiate the auto coloration
    initiate(autoreset=True)

    parser = argparse.ArgumentParser(
        description="The tool to clean a list or a hosts file "
        "with the Ultimate Hosts Blacklist whitelist list or your own.",
        epilog="Crafted with %s by %s"
        % (
            Fore.RED + "♥" + Fore.RESET,
            Style.BRIGHT + Fore.CYAN + "Nissar Chababy (Funilrys) " + Style.RESET_ALL,
        ),
    )

    parser.add_argument(
        "-a",
        "--anti-whitelist",
        type=argparse.FileType("r"),
        nargs="+",
        help="Read the given file and remove the rules (its data) "
        "from the whitelist list we are going to use.",
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
        type=argparse.FileType("r"),
        help="Read the given file and remove all element to whitelist.",
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
        help="Save the result to the given filename or path.",
    )

    parser.add_argument(
        "-m",
        "--multiprocessing",
        action="store_true",
        default=False,
        help="Activate the usage of multiple processes.",
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
        help="The number of (maximal) processes to use.",
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
        type=argparse.FileType("r"),
        nargs="+",
        help="Read the given file and append its data to the our whitelist list.",
    )

    parser.add_argument(
        "-wc",
        "--without-core",
        action="store_false",
        help="Disable the usage of the Ultimate Hosts Blacklist whitelist list.",
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
            ).filter(
                file=arguments.file,
                standard_sort=arguments.standard_sorting,
                hierarchical_sort=arguments.hierachical_sorting,
            )
