The whitelisting tool from the Ultimate Hosts Blacklist project
===============================================================

This is the whitelisting tool provided by the Ultimate Hosts Blacklist project.
It is mainly used to whitelist subject (domains, IP, URL) into our infrastructure but can also be used outside our infrastructure.

Indeed, this tool allows you:

* to get rid of our whitelist.
* to use your own whitelist.
* to use your own whitelist along with our whitelist.
* to get rid of one of the rule mentionned in our whitelist.
* to have a whitelist tool ready to use as a Python module.


Installation
------------

::

    $ pip3 install --user ultimate-hosts-blacklist-whitelist



Complementary whitelist
-----------------------

Our tool allow us to link one or more file(s) to the system which will be used in complementary of our whitelist list.

Special markers
---------------

If you already used a whitelist list you already know that we generaly only list all domains we want to whitelist one by one.

It's also possible to do that with our whitelisting system but we can do more.

:code:`ALL`
^^^^^^^^^^^

The :code:`ALL` marker will tell the system to escape and regex check against what follows.

INVALID characters
""""""""""""""""""

* :code:`$`

    * As we automatically append :code:`$` to the end, you should not use this character.

* :code:`\\`

    * As we automatically escape the given expression, you should not explicitly escape your regular expression when declaring an :code:`ALL` marker.

:code:`REG`
"""""""""""

The :code:`REG` marker will tell the system to explicitly check for the given regex which follows the marker.

:code:`RZD`
"""""""""""

The :code:`RZD` marker will tell the system to explicitly check for the given string plus all possible TDL.

Anti whitelist
--------------

Don't like one of our rule ? Our tool allows you to specify a file which contain a list of rule you don't want to apply.

Simply use the :code:`--anti-whitelist` flag to tell us one or more anti whitelist files and we will apply!


Understanding what we actually do
---------------------------------

If we have the following secondary whitelist list:

::

    facebook.com
    ALL .gov
    REG face
    RZD example

our system will actually :

* Remove every line which match :code:`facebook.com` and :code:`www.facebook.com`
* Remove everyline which match :code:`example.*`
* In complementary convert all lines with :code:`ALL ` or :code:`REG` to the right format.
* Check every line against the regular expression.
* Print or save on screen the results.

The generated regular expression will be in this example:

::

    (\.gov$)|(face)|(example(.*))


.. note::
    The :code:`example` group is much longer as we construct the list of TDL based on the Root Zone Database of the IANA and the Public Suffix List project.**

Which actually means that we whitelist:

* all elements/lines which ends with :code:`.gov`
* all elements/lines which contain the word :code:`face`
* all possible TDL combinaison which starts with :code:`example`

Contributors
------------

* Daniel - `@dnmTX`_

Usage of the tool
-----------------

The sript can be called as :code:`uhb-whitelist`, :code:`uhb_whitelist` and :code:`ultimate-hosts-blacklist-whitelist`.

::

    usage: uhb_whitelist [-h] [-a ANTI_WHITELIST [ANTI_WHITELIST ...]] [-d]
                        [-f FILE] [-o OUTPUT] [-m] [-p PROCESSES] [-v]
                        [-w WHITELIST [WHITELIST ...]] [-wc]

    The tool to clean a list or a hosts file with the Ultimate Hosts Blacklist
    whitelist list or your own.

    optional arguments:
        -h, --help            show this help message and exit
        -a ANTI_WHITELIST [ANTI_WHITELIST ...], --anti-whitelist ANTI_WHITELIST [ANTI_WHITELIST ...]
                                Read the given file and remove the rules (its data)
                                from the whitelist list we are going to use.
        -d, --debug           Activate the debug mode. This mode will write the
                                whole processes to stdout.
        -f FILE, --file FILE  Read the given file and remove all element to
                                whitelist.
        -o OUTPUT, --output OUTPUT
                                Save the result to the given filename or path.
        -m, --multiprocessing
                                Activate the usage of multiple processes.
        -p PROCESSES, --processes PROCESSES
                                The number of (maximal) processes to use.
        -v, --version         Show the version end exist.
        -w WHITELIST [WHITELIST ...], --whitelist WHITELIST [WHITELIST ...]
                                Read the given file and append its data to the our
                                whitelist list.
        -wc, --without-core   Disable the usage of the Ultimate Hosts Blacklist
                                whitelist list.

    Crafted with ♥ by Nissar Chababy (Funilrys)


License
-------

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

.. _@dnmTX: https://github.com/dnmTX