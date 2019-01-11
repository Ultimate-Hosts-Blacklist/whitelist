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
from update import Helpers, Settings, path, strftime
from whitelisting import Whitelist

INFO = {}


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


def generate_clean_and_whitelisted_list():
    """
    Update/Create `clean.list` and `whitelisted.list`.
    """

    if bool(int(INFO["clean_original"])):
        clean_list = []

        list_special_content = Helpers.Regex(
            Helpers.File(Settings.file_to_test + Settings.list_name).to_list(), r"ALL\s"
        ).matching_list()

        active = Settings.current_directory + "output/domains/ACTIVE/list"

        if path.isfile(active):
            clean_list.extend(
                Helpers.Regex(Helpers.File(active).to_list(), r"^#").not_matching_list()
                + list_special_content
            )

        clean_list = Helpers.List(clean_list).format()
        whitelisted = Whitelist(string="\n".join(clean_list)).get()

        Helpers.File(Settings.clean_list_file).write(
            "\n".join(clean_list), overwrite=True
        )

        Helpers.File(Settings.whitelisted_list_file).write(whitelisted, overwrite=True)

        Helpers.File("whitelisting.py").delete()


if __name__ == "__main__":
    get_administration_file()
    update_adminisation_file()
    save_administration_file()

    generate_clean_and_whitelisted_list()
