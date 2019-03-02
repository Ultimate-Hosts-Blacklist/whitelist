#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module has been written in order to be the main entry for every tests in a
directory which contain a list to test.


Authors:
    - @Funilrys, Nissar Chababy <contactTAfunilrysTODcom>
    - @mitchellkrogza, Mitchell Krog <mitchellkrogTAgmailTODcom

Contributors:
    Let's contribute !

    @GitHubUsername, Name, Email (optional)
"""
# pylint: disable=bad-continuation, too-many-lines
from json import decoder, dump, loads
from os import environ, getcwd, path, remove
from os import sep as directory_separator
from os import walk
from re import compile as comp
from re import escape
from re import sub as substrings
from shutil import copyfileobj, rmtree
from subprocess import PIPE, Popen
from tarfile import open as tarfile_open
from time import ctime, strftime

from domain2idna import get as domain2idna
from requests import get


class Settings:  # pylint: disable=too-few-public-methods
    """
    This class will save all data that can be called from anywhere in the code.
    """

    # This variable will help us keep a track on info.json content.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    informations = {}

    # This variable should be initiated with the raw link to the hosts file or the
    # list we are going to test.
    #
    # Note: The variable name should not be changed.
    # Note: This variable is auto updated by Initiate()
    #
    # Example:
    # "https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt"
    raw_link = ""

    # This variable should be initiated with the name of the list once downloaded.
    # Recommended formats:
    #  - GitHub Repository:
    #    - GitHubUsername@RepoName.list
    #  - GitHub organization:
    #    - GitHubOrganisationName@RepoName.list
    #  - Others:
    #    - websiteDomainName.com@listName.list
    #
    # Note: The variable name should not be changed.
    #
    # Example: "adaway.github.io@AdAway.list"
    list_name = "domains.list"

    # This variable is used to set the location of the file for the list without
    # dead/inactive domains.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    # Note: This variable is auto updated by Initiate()
    clean_list_file = "clean.list"

    # This variable is used to set the location of the file for the list without
    # dead/inactive domains and whitelisted domains.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    # Note: This variable is auto updated by Initiate()
    whitelisted_list_file = "whitelisted.list"

    # This variable is used to set the location of the file for the list without
    # dead/inactive domains.
    # The difference between the purpose of this file and the clean.list file
    # is that this file do not take the "SPECIAL" flag of PyFunceble in
    # consideration.
    volatile_list_file = "volatile.list"

    # This variable will help us know where we are working into the filesystem.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    current_directory = getcwd() + directory_separator

    # This variable will help us know which file we are going to test.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    # Note: This variable is auto updated by Initiate()
    file_to_test = current_directory + list_name

    # This variable will help us know what how many days we have to wait until next test.
    #
    # Note: This variable is auto updated by Initiate()
    days_until_next_test = 0

    # This variable will help us know the date of the last test.
    #
    # Note: This variable is auto updated by Initiate()
    last_test = 0

    # This variable will help us manage the implementation of days_until_next_test and last_test.
    #
    # Note: This variable is auto updated by Initiate()
    currently_under_test = False

    # This variable will help us know where should the info.json file be located.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    repository_info = current_directory + "info.json"

    # This variable will help us know which version of PyFunceble we are going to use.
    #
    # Note: True = master | False = dev
    # Note: This variable is auto updated by Initiate()
    stable = False

    # This variable represent the PyFunceble infrastructure.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    PyFunceble = {
        ".PyFunceble_production.yaml": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/.PyFunceble_production.yaml",  # pylint: disable=line-too-long
        ".PyFunceble_LICENSE": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/LICENSE",  # pylint: disable=line-too-long
    }

    # This variable is used to match [ci skip] from the git log.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    regex_travis = "[ci skip]"

    # This variable is used ot match the special whitelist elements.
    regex_whitelist = r"(ALL|REG|RZD)\s"

    # This variable is used to set the number of minutes before we stop the script under Travis CI.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    # Note: This variable is auto updated by Initiate()
    autosave_minutes = 15

    # This variable is used to set the default commit message when we commit
    # under Travic CI.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    # Note: This variable is auto updated by Initiate()
    commit_autosave_message = ""

    # This variable is used to set permanent_license_link.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    permanent_license_link = "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/repository-structure/master/LICENSE"  # pylint: disable=line-too-long

    # This variable is used to set the permanant config links
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    permanent_config_link = "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/repository-structure/master/.PyFunceble_cross_input_sources.yaml"  # pylint: disable=line-too-long

    # This variable is used to set the arguments when executing PyFunceble.py
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    # Note: This variable is auto updated by Initiate()
    arguments = []

    # This variable is used to know if we need to delete INACTIVE and INVALID
    # domain from the original file.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    # Note: This variable is auto updated by Initiate()
    clean_original = False

    # This variable is used to know if we need to convert the list into idna
    # before we write the file PyFunceble is going to test.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    # Note: This variable is auto updated by Initiate()
    convert_to_idna = True

    # This variable is used to know the marker which we have to match in
    # order to start from the begining.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    launch_test_marker = r"Launch\stest"

    # This variable set the name of the administration file.
    #
    # Note: DO NOT TOUCH UNLESS YOU KNOW WHAT IT MEANS!
    administration_script = "administration.py"


class TravisCI:
    """
    Manage everything needed when working with
    Travis CI.
    """

    @classmethod
    def configure_git(cls):
        """
        Prepare Git for push.
        """

        try:
            _ = environ["TRAVIS_BUILD_DIR"]

            Helpers.Command("git remote rm origin", False).execute()
            Helpers.Command(
                "git remote add origin https://"
                + "%s@github.com/%s.git"
                % (environ["GH_TOKEN"], environ["TRAVIS_REPO_SLUG"]),
                False,
            ).execute()
            Helpers.Command(
                'git config --global user.email "%s"' % (environ["GIT_EMAIL"]), False
            ).execute()
            Helpers.Command(
                'git config --global user.name "%s"' % (environ["GIT_NAME"]), False
            ).execute()
            Helpers.Command("git config --global push.default simple", False).execute()
            Helpers.Command("git checkout %s" % environ["GIT_BRANCH"], False).execute()

        except KeyError:
            pass

    @classmethod
    def fix_permissions(cls):
        """
        Fix the permissions of the TRAVIS_BUILD_DIR.
        """

        try:
            build_dir = environ["TRAVIS_BUILD_DIR"]
            commands = [
                "sudo chown -R travis:travis %s" % (build_dir),
                "sudo chgrp -R travis %s" % (build_dir),
                "sudo chmod -R g+rwX %s" % (build_dir),
                "sudo chmod 777 -Rf %s.git" % (build_dir + directory_separator),
                r"sudo find %s -type d -exec chmod g+x '{}' \;" % (build_dir),
            ]

            for command in commands:
                Helpers.Command(command, False).execute()

            if (
                Helpers.Command("git config core.sharedRepository", False).execute()
                == ""
            ):
                Helpers.Command(
                    "git config core.sharedRepository group", False
                ).execute()
        except KeyError:
            pass

    def __init__(self, init_instance=False):
        if init_instance:
            self.configure_git()


class PyFunceble:
    """
    Manage the way we work and execute PyFunceble.
    """

    @classmethod
    def install(cls):
        """
        Install the right version of PyFunceble.
        """

        if Settings.stable:
            to_download = "PyFunceble"
        else:
            to_download = "PyFunceble-dev"

        Helpers.Command("pip3 install %s" % to_download, False).execute()

    @classmethod
    def download_complementary_files(cls):
        """
        Download all complementary PyFunceble's related files.
        """

        for file in Settings.PyFunceble:
            file_path = Settings.current_directory + file

            if not Settings.stable:
                download_link = Settings.PyFunceble[file].replace("master", "dev")
            else:
                download_link = Settings.PyFunceble[file].replace("dev", "master")

            if not Helpers.Download(download_link, file_path).link():
                raise Exception("Unable to download %s." % download_link)

        Helpers.File(Settings.current_directory + "tool.py").delete()
        Helpers.File(Settings.current_directory + "PyFunceble.py").delete()
        Helpers.File(Settings.current_directory + "requirements.txt").delete()

    @classmethod
    def clean(cls):
        """
        Clean the output directory if present.
        """

        if path.isdir(Settings.current_directory + "output"):
            Helpers.Command("PyFunceble --clean", False).execute()

    @classmethod
    def construct_arguments(cls):
        """
        Construct the arguments to pass to PyFunceble.
        """

        to_use = []

        to_use.append(
            "--cmd-before-end %s" % Settings.current_directory
            + Settings.administration_script
        )

        if Settings.convert_to_idna:
            to_use.append("--idna")

        if Settings.arguments != []:
            to_use.extend(Settings.arguments)

        if to_use:
            return " ".join(to_use)

        return ""

    @classmethod
    def is_test_allowed(cls):
        """
        Authorize a test run.
        """

        if Helpers.Regex(
            Helpers.Command("git log -1", False).execute(),
            Settings.launch_test_marker,
            return_data=False,
            escape=False,
        ).match():
            cls.clean()
            return True

        if not Settings.currently_under_test:
            cls.clean()
            return True

        if Settings.days_until_next_test >= 1 and Settings.last_test != 0:
            retest_date = Settings.last_test + (
                24 * Settings.days_until_next_test * 3600
            )

            if int(strftime("%s")) >= retest_date or Settings.currently_under_test:
                return True

            return False

        return True

    @classmethod
    def run(cls):
        """
        Run PyFunceble.
        """
        # pylint: disable=invalid-name
        PyFunceble_path = "PyFunceble"

        command_to_execute = "%s -v && " % (PyFunceble_path)

        try:
            command_to_execute += (
                "export TRAVIS_BUILD_DIR=%s && " % environ["TRAVIS_BUILD_DIR"]
            )
        except KeyError:
            pass

        command_to_execute += "%s %s -f %s" % (
            PyFunceble_path,
            cls.construct_arguments(),
            Settings.file_to_test,
        )

        if cls.is_test_allowed():
            Helpers.Download(
                Settings.permanent_license_link, Settings.current_directory + "LICENSE"
            ).link()

            Settings.informations.update(
                {"last_test": strftime("%s"), "currently_under_test": str(int(True))}
            )

            for index in ["clean_list_file", "list_name"]:
                if index in Settings.informations:
                    del Settings.informations[index]

            Helpers.Dict(Settings.informations).to_json(Settings.repository_info)

            Helpers.Command(command_to_execute, True).execute()

        else:
            print(
                "No need to test until %s."
                % ctime(
                    Settings.last_test + (24 * Settings.days_until_next_test * 3600)
                )
            )
            exit(0)

    class Configuration:
        """
        Manage the way we generate and install the PyFunceble's configuration.
        """

        @classmethod
        def update(cls):
            """
            Update the cross repository configuration.
            """

            if path.isfile(Settings.permanent_config_link.split("/")[-1]):
                if not Settings.stable:
                    to_download = Settings.PyFunceble[
                        ".PyFunceble_production.yaml"
                    ].replace("master", "dev")
                else:
                    to_download = Settings.PyFunceble[
                        ".PyFunceble_production.yaml"
                    ].replace("dev", "master")

                destination = Settings.permanent_config_link.split("/")[-1]

                if path.isfile(destination):
                    Helpers.Download(to_download, destination).link()

                    to_replace = {
                        r"less:.*": "less: False",
                        r"plain_list_domain:.*": "plain_list_domain: True",
                        r"seconds_before_http_timeout:.*": "seconds_before_http_timeout: 6",
                        r"share_logs:.*": "share_logs: True",
                        r"show_execution_time:.*": "show_execution_time: True",
                        r"split:.*": "split: True",
                        r"travis:.*": "travis: True",
                        r"travis_autosave_commit:.*": 'travis_autosave_commit: "[Autosave] Testing for Ultimate Hosts Blacklist"',  # pylint: disable=line-too-long
                        r"travis_autosave_final_commit:.*": 'travis_autosave_final_commit: "[Results] Testing for Ultimate Hosts Blacklist"',  # pylint: disable=line-too-long
                        r"travis_branch:.*": "travis_branch: master",
                        r"travis_autosave_minutes:.*": "travis_autosave_minutes: %s"
                        % Settings.autosave_minutes,
                    }

                    content = Helpers.File(destination).read()

                    for regex, replacement in to_replace.items():
                        content = Helpers.Regex(
                            content, regex, replace_with=replacement, return_data=True
                        ).replace()

                    Helpers.File(destination).write(content, overwrite=True)
                    Helpers.File(".PyFunceble.yaml").write(content, overwrite=True)

        @classmethod
        def install(cls):
            """
            Install the cross repository configuration.
            """

            if not path.isfile(Settings.permanent_config_link.split("/")[-1]):
                Helpers.Download(
                    Settings.permanent_config_link, ".PyFunceble.yaml"
                ).link()


class DomainsList:
    """
    Construct, generate or update the domains.list file.
    """

    @classmethod
    def format_domain(cls, extracted_domain):
        """
        Format the extracted domain before passing it to the system.

        Argument:
            - extracted_domain: str
                The extracted domain or line from the file.
        """

        extracted_domain = extracted_domain.strip()

        if not extracted_domain.startswith("#"):

            if "#" in extracted_domain:
                extracted_domain = extracted_domain[
                    : extracted_domain.find("#")
                ].strip()

            if " " in extracted_domain or "\t" in extracted_domain:
                splited_line = extracted_domain.split()

                for element in splited_line[1:]:
                    if element:
                        return element

            return extracted_domain

        return ""

    @classmethod
    def extract_lines(cls, file):
        """
        This method extract and format each line to get the domain.

        Argument:
            - file: str
                The file to read.
        """

        from PyFunceble import is_subdomain, syntax_check

        result = []

        for line in Helpers.File(file).to_list():
            if not line:
                continue

            if line.startswith("#"):
                continue

            if Helpers.Regex(line, Settings.regex_whitelist, return_data=False).match():
                result.append(line)
                continue

            formated = cls.format_domain(line.strip())

            if formated.startswith("www."):
                if formated[4:] not in result:
                    result.append(formated[4:])
            elif syntax_check(domain2idna(formated)) and not is_subdomain(
                domain2idna(formated)
            ):
                new_version = f"www.{formated}"

                if new_version not in result:
                    result.append(new_version)

            result.append(formated)

        return result

    @classmethod
    def generate_from_tar_gz(cls):
        """
        This method will search download and decompress .tar.gz.
        + searches for `domains` files.
        """

        download_filename = Settings.raw_link.split("/")[-1]
        extraction_directory = "./temp"

        if Helpers.Download(Settings.raw_link, download_filename).link():
            Helpers.File(download_filename).tar_gz_decompress(extraction_directory)

            formated_content = []

            for root, dirs, files in walk(  # pylint: disable=unused-variable
                extraction_directory
            ):
                for file in files:
                    if file.startswith("domains"):
                        formated_content.extend(
                            cls.extract_lines(path.join(root, file))
                        )

            formated_content = Helpers.List(formated_content).format()

            Helpers.File(Settings.list_name).write(
                "\n".join(formated_content), overwrite=True
            )

            Helpers.Directory(extraction_directory).delete()
            Helpers.File(download_filename).delete()

        else:
            raise Exception("Unable to download the the file. Please check the link.")

    @classmethod
    def construct(cls):
        """
        Construct or update the file we are going to test.
        """

        restart = (
            Helpers.Regex(
                Helpers.Command("git log -1", False).execute(),
                Settings.launch_test_marker,
                return_data=False,
                escape=False,
            ).match()
            or not Settings.currently_under_test
        )

        if restart:
            if Settings.raw_link.endswith(".tar.gz"):
                cls.generate_from_tar_gz()
            elif Helpers.Download(Settings.raw_link, Settings.file_to_test).link():
                Helpers.Command("dos2unix " + Settings.file_to_test, False).execute()

                formated_content = Helpers.List(
                    cls.extract_lines(Settings.file_to_test)
                ).format()

                Helpers.File(Settings.file_to_test).write(
                    "\n".join(formated_content), overwrite=True
                )

                del formated_content
            elif not Settings.raw_link and path.isfile(Settings.file_to_test):
                print("\n")
                new_file_content = Helpers.List(
                    cls.extract_lines(Settings.file_to_test)
                ).format()

                Helpers.File(Settings.file_to_test).write(
                    "\n".join(new_file_content), overwrite=True
                )

                del new_file_content

            if restart:
                Settings.currently_under_test = False

            PyFunceble.clean()


class Administration:
    """
    Administration file/info manipulation.
    """

    @classmethod
    def update_settings(cls, index):
        """
        Update Setting.index.

        Argument:
            - index: str
                A valid index name.
        """

        try:
            getattr(Settings, index)
            if (
                index
                in [
                    "stable",
                    "currently_under_test",
                    "clean_original",
                    "convert_to_idna",
                ]
                and Settings.informations[index].isdigit()
            ):
                setattr(Settings, index, bool(int(Settings.informations[index])))
            elif (
                index in ["days_until_next_test", "last_test", "autosave_minutes"]
                and Settings.informations[index].isdigit()
            ):
                setattr(Settings, index, int(Settings.informations[index]))
            else:
                setattr(Settings, index, Settings.informations[index])
        except AttributeError:
            raise Exception(
                '"%s" into %s is unknown.' % (index, Settings.repository_info)
            )

    @classmethod
    def parse_file(cls):
        """
        Parse the administation file.
        """

        if path.isfile(Settings.repository_info):
            content = Helpers.File(Settings.repository_info).read()
            Settings.informations = Helpers.Dict().from_json(content)
            to_ignore = ["raw_link", "name"]

            for index in Settings.informations:
                if Settings.informations[index] != "":
                    if index not in to_ignore[1:]:
                        cls.update_settings(index)
                elif index in to_ignore:
                    continue
                else:
                    raise Exception(
                        'Please complete "%s" into %s'
                        % (index, Settings.repository_info)
                    )
        else:
            raise Exception(
                "Impossible to read %s" % Settings.current_directory + "info.json"
            )

    def __call__(self):
        """
        Prepare the repository structure.
        """

        travis = TravisCI(init_instance=True)
        travis.fix_permissions()

        PyFunceble.Configuration.update()
        PyFunceble.Configuration.install()

        self.parse_file()

        PyFunceble.install()
        PyFunceble.download_complementary_files()

        DomainsList.construct()
        travis.fix_permissions()

        PyFunceble.run()


class Helpers:  # pylint: disable=too-few-public-methods
    """
    Well thanks to those helpers I wrote :)
    """

    class Dict:
        """
        Dictionary manipulations.

        Argument:
            - main_dictionnary: dict
                The main_dictionnary to pass to the whole class.
        """

        def __init__(self, main_dictionnary=None):

            if main_dictionnary is None:
                self.main_dictionnary = {}
            else:
                self.main_dictionnary = main_dictionnary

        def to_json(self, destination):
            """
            Save a dictionnary into a JSON file.

            Argument:
                - destination: str
                    A path to a file where we're going to Write the
                    converted dict into a JSON format.
            """

            with open(destination, "w") as file:
                dump(
                    self.main_dictionnary,
                    file,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=True,
                )

        @classmethod
        def from_json(cls, data):
            """
            Convert a JSON formated string into a dictionary.

            Argument:
                data: str
                    A JSON formeted string to convert to dict format.
            """

            try:
                return loads(data)

            except decoder.JSONDecodeError:
                return {}

    class List:  # pylint: disable=too-few-public-methods
        """
        List manipulation.
        """

        def __init__(self, main_list=None):
            if main_list is None:
                self.main_list = []
            else:
                self.main_list = main_list

        def format(self):
            """
            Return a well formated list. Basicaly, it's sort a list and remove duplicate.
            """

            try:
                return sorted(list(set(self.main_list)), key=str.lower)

            except TypeError:
                return self.main_list

    class Directory:  # pylint: disable=too-few-public-methods
        """
        Directory treatment/manipulations.

        Argument:
            - directory: str
                A path to the directory to manipulate.
        """

        def __init__(self, directory):
            self.directory = directory

        def delete(self):
            """
            This method delete the given directory.
            """

            try:
                rmtree(self.directory)
            except FileNotFoundError:
                pass

    class File:  # pylint: disable=too-few-public-methods
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

            for read in open(self.file, encoding="utf-8"):
                result.append(read.rstrip("\n").strip())

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

        def delete(self):
            """
            Delete a given file path.
            """

            try:
                remove(self.file)
            except OSError:
                pass

        def tar_gz_decompress(self, destination):
            """
            Decompress a given file into the given destination.

            Argument:
                - destination: str
                    The destination of the decompressed.
            """

            if destination is not None and isinstance(destination, str):
                with tarfile_open(self.file) as thetar:
                    thetar.extractall(path=destination)

    class Download:  # pylint: disable=too-few-public-methods
        """
        This class will initiate a download of the desired link.

        Arguments:
            - link_to_download: str
                The link to the file we are going to download.
            - destination: str
                The destination of the downloaded data.
        """

        def __init__(self, link_to_download, destination):
            self.link_to_download = link_to_download
            self.destination = destination

        def link(self):
            """
            This method initiate the download.
            """

            if self.link_to_download:
                request = get(self.link_to_download, stream=True)

                if request.status_code == 200:
                    with open(self.destination, "wb") as file:
                        request.raw.decode_content = True
                        copyfileobj(request.raw, file)

                    del request

                    return True

            return False

    class Command:
        """
        Shell command execution.

        Arguments:
            - command: str
                The command to execute.
            - allow_stdout: bool
                If true stdout is always printed otherwise stdout is passed
                to PIPE.
        """

        def __init__(self, command, allow_stdout=True):
            self.decode_type = "utf-8"
            self.command = command
            self.stdout = allow_stdout

        def decode_output(self, to_decode):
            """Decode the output of a shell command in order to be readable.

            Argument:
                - to_decode: byte
                    Output of a command to decode.
            """
            if to_decode is not None:
                # return to_decode.decode(self.decode_type)
                return str(to_decode, self.decode_type)

            return False

        def execute(self):
            """
            Execute the given command.
            """

            if not self.stdout:
                process = Popen(self.command, stdout=PIPE, stderr=PIPE, shell=True)
            else:
                process = Popen(self.command, stderr=PIPE, shell=True)

            (output, error) = process.communicate()

            if process.returncode != 0:
                decoded = self.decode_output(error)

                if not decoded:
                    return "Unkown error. for %s" % (self.command)

                print(decoded)
                exit(1)
            return self.decode_output(output)

    class Regex:  # pylint: disable=too-few-public-methods

        """A simple implementation ot the python.re package

        Arguments:
            - data: str
                The data to regex check.
            - regex: str
                The regex to match.
            - group: int
                The group to return
            - rematch: bool
                True: return the matched groups into a formated list.
                    (implementation of Bash ${BASH_REMATCH})
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
                "rematch": False,
                "replace_with": None,
                "return_data": True,
            }

            # We initiate our optional_arguments in order to be usable all over the
            # class
            for (arg, default) in optional_arguments.items():
                setattr(self, arg, args.get(arg, default))

            if self.escape:  # pylint: disable=no-member
                self.regex = escape(regex)
            else:
                self.regex = regex

        def not_matching_list(self):
            """
            This method return a list of string which don't match the
            given regex.
            """

            pre_result = comp(self.regex)

            return list(
                filter(lambda element: not pre_result.search(str(element)), self.data)
            )

        def matching_list(self):
            """
            This method return a list of the string which match the given
            regex.
            """

            pre_result = comp(self.regex)

            return list(
                filter(lambda element: pre_result.search(str(element)), self.data)
            )

        def match(self):
            """
            Used to get exploitable result of re.search
            """

            # We initate this variable which gonna contain the returned data
            result = []

            # We compile the regex string
            to_match = comp(self.regex)

            # In case we have to use the implementation of ${BASH_REMATCH} we use
            # re.findall otherwise, we use re.search
            if self.rematch:  # pylint: disable=no-member
                pre_result = to_match.findall(self.data)
            else:
                pre_result = to_match.search(self.data)

            if self.return_data and pre_result:  # pylint: disable=no-member
                if self.rematch:  # pylint: disable=no-member
                    for data in pre_result:
                        if isinstance(data, tuple):
                            result.extend(list(data))
                        else:
                            result.append(data)

                    if self.group != 0:  # pylint: disable=no-member
                        return result[self.group]  # pylint: disable=no-member

                else:
                    result = pre_result.group(
                        self.group  # pylint: disable=no-member
                    ).strip()

                return result

            elif not self.return_data and pre_result:  # pylint: disable=no-member
                return True

            return False

        def replace(self):
            """
            Used to replace a matched string with another.
            """

            if self.replace_with:  # pylint: disable=no-member
                return substrings(
                    self.regex,
                    self.replace_with,  # pylint: disable=no-member
                    self.data,
                    self.occurences,  # pylint: disable=no-member
                )

            return self.data


if __name__ == "__main__":
    REPOSITORY_UPDATE = Administration()
    REPOSITORY_UPDATE()
