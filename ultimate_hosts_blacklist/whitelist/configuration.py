"""
The whitelist script of the Ultimate-Hosts-Blacklist project.

Provide some configurable variables.

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
# pylint: disable=too-few-public-methods


class Configuration:
    """
    Provice some configuration varieables.
    """

    # List of all markers we can use.
    markers = {"all": "ALL ", "regex": "REG ", "root_zone_db": "RZD "}

    # List fo all links we may use.
    links = {
        "core": "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/whitelist/master/domains.list",  # pylint: disable=line-too-long
        "root_zone_db": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/iana-domains-db.json",  # pylint: disable=line-too-long
        "public_suffix": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/public-suffix.json",  # pylint: disable=line-too-long
    }
