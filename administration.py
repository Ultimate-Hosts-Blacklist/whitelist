#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is just a module for administration purpose.
The idea is to leave PyFunceble run this script in order to get less headache
while debugging environnements.

Authors:
    - @Funilrys, Nissar Chababy <contactTAfunilrysTODcom>

Contributors:
    Let's contribute !

    @GitHubUsername, Name, Email (optional)
"""
# pylint:disable=bad-continuation

from PyFunceble import is_subdomain
from ultimate_hosts_blacklist_the_whitelist import clean_list_with_official_whitelist

from update import Helpers, Settings, path, strftime

INFO = {}


PYFUNCEBLE_CONFIGURATION = {"no_whois": True}
PYFUNCEBLE_CONFIGURATION_VOLATILE = {"no_whois": True, "no_special": True}
REGEX_SPECIAL = r"\.blogspot\.|\.liveadvert\.com$|\.skyrock\.com$|\.tumblr\.com$|\.wordpress\.com$|\.doubleclick\.net$"  # pylint: disable=line-too-long


def get_administration_file():
    """
    Get the administation file content.
    """

    if path.isfile(Settings.repository_info):
        content = Helpers.File(Settings.repository_info).read()
        INFO.update(Helpers.Dict().from_json(content))
    else:
        raise Exception("Unable to find the administration file.")


def update_adminisation_file():
    """
    Update what should be updated.
    """

    INFO.update({"currently_under_test": str(int(False)), "last_test": strftime("%s")})


def save_administration_file():
    """
    Save the current state of the administration file content.
    """

    Helpers.Dict(INFO).to_json(Settings.repository_info)


def generate_extra_files():  # pylint: disable=too-many-branches,too-many-statements
    """
    Update/Create `clean.list`, `volatile.list` and `whitelisted.list`.
    """

    if bool(int(INFO["clean_original"])):  # pylint: disable=too-many-nested-blocks
        clean_list = []
        temp_clean_list = []
        volatile_list = []

        list_special_content = Helpers.Regex(
            Helpers.File(Settings.file_to_test).to_list(), r"(ALL|REG|RZD)\s"
        ).matching_list()

        active = Settings.current_directory + "output/domains/ACTIVE/list"
        inactive = Settings.current_directory + "output/domains/INACTIVE/list"

        if path.isfile(active):
            print("Starting manipulation of `{}`.".format(active))
            temp_clean_list.extend(
                Helpers.Regex(Helpers.File(active).to_list(), r"^#").not_matching_list()
                + list_special_content
            )
            print("Stoping manipulation of `{}`.".format(active))

        if path.isfile(inactive):
            print("Starting manipulation of `{}`.".format(inactive))

            for element in Helpers.Regex(
                Helpers.File(inactive).to_list(), REGEX_SPECIAL
            ).matching_list():
                if element:
                    if not is_subdomain(element):
                        if element.startswith("www."):
                            volatile_list.append(element[4:])
                        else:
                            volatile_list.append("www.{}".format(element))
                    volatile_list.append(element)
            print("Stoping manipulation of `{}`.".format(inactive))

        temp_clean_list = Helpers.List(temp_clean_list).format()

        print(
            "Starting the generation of the content of `{}`.".format(
                Settings.clean_list_file
            )
        )
        for element in temp_clean_list:
            if element:
                if not is_subdomain(element):
                    if element.startswith("www."):
                        clean_list.append(element[4:])
                    else:
                        clean_list.append("www.{}".format(element))
                clean_list.append(element)
        print(
            "Stoping the generation of the content of `{}`.".format(
                Settings.clean_list_file
            )
        )

        print("Deletion of duplicate for `{}`".format(Settings.clean_list_file))
        clean_list = Helpers.List(clean_list).format()
        print(
            "Generation of the content of `{}`".format(Settings.whitelisted_list_file)
        )
        whitelisted = clean_list_with_official_whitelist(clean_list)

        volatile_list.extend(clean_list)
        volatile_list = Helpers.List(volatile_list).format()

        print("Writing `{}`".format(Settings.clean_list_file))
        Helpers.File(Settings.clean_list_file).write(
            "\n".join(clean_list), overwrite=True
        )

        print("Writing `{}`".format(Settings.whitelisted_list_file))
        Helpers.File(Settings.whitelisted_list_file).write(
            "\n".join(whitelisted), overwrite=True
        )

        print("Writing `{}`".format(Settings.volatile_list_file))
        Helpers.File(Settings.volatile_list_file).write(
            "\n".join(volatile_list), overwrite=True
        )

        Helpers.File("whitelisting.py").delete()


if __name__ == "__main__":
    get_administration_file()
    update_adminisation_file()
    save_administration_file()

    generate_extra_files()
