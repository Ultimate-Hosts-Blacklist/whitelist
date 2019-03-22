"""
The whitelist script of the Ultimate-Hosts-Blacklist project.

Provide the matching class which is used to check rules.

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
from ultimate_hosts_blacklist.helpers import Regex


class Match:
    """
    Provide the matching logic.
    """

    @classmethod
    def ends(cls, line, rule):
        """
        Check if the given line match the given (ends) rule.
        """

        return line.endswith(rule)

    @classmethod
    def strict(cls, line, rule):
        """
        Check if the given line match the given (strict) rule.
        """

        if " " in line or "\t" in line:
            if line.endswith(" {0}".format(rule)):
                return True
            if line.endswith("\t{0}".format(rule)):
                return True
        else:
            if line == rule:
                return True
        return False

    @classmethod
    def regex(cls, line, rule):
        """
        Check if the given line match the given (regex) rule.
        """

        return Regex(line, rule, return_data=False).match()

    @classmethod
    def present(cls, line, rule):
        """
        Check if the given line match the given (present) rule.
        """

        return line in rule
