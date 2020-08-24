The whitelisting tool from the Ultimate Hosts Blacklist project
===============================================================

This is the whitelisting tool provided by the Ultimate Hosts Blacklist project.
The script is mainly used to whitelist subject (domains, IP, URL) into our
infrastructure but it can also easily be used outside our infrastructure.

The ultimate hosts blacklist whitelist (**UHBW**) tool allows you:

* to append your own whitelist as complementary to our whitelist.

::

    uhb_whitelist -f inputfile -o outputfile -w whitelistfile



* to anti-whitelist (reverse) only particular domains while still using our core list.

::

    uhb_whitelist -f inputfile -o outputfile --anti-whitelist antiwhitelistfile



* to whitelist and anti-whitelist while still using our core list.

::

    uhb_whitelist -f inputfile -o outputfile --anti-whitelist antiwhitelistfile -w whitelistfile



* to override our core whitelist whilst still applying your own personal whitelist and anti-whitelist.

::

    uhb_whitelist -f inputfile -o outputfile --anti-whitelist antiwhitelistfile -w whitelistfile -wc


* to have a whitelist tool ready to use as a Python module.


Installation
------------

::

    $ pip3 install --user ultimate-hosts-blacklist-whitelist



The hosted whitelist
--------------------

The hosted whitelist can be found at `whitelist`_
This white-list is maintained by the team of good peoples behind the `whitelist`_
project.

Complementary whitelist
-----------------------

`UHBW`_ allows you to link one or more file(s) to the system which will be used as
complementary to the hosted `whitelist`_, which is downloaded and used by default.

Special markers
---------------

If you already have tried to use a whitelist, you'll probably know, that in
generally you can only add one domain or URL per line in a file, for which you
want to whitelist.

With UHBW you can do this, but in addition to that tedious way, UHBW allows you
to use ``Regex``, :code:`RZD` and :code:`ALL`

:code:`ALL`
^^^^^^^^^^^

The :code:`ALL` marker will tell the system to escape and regex check against
what follows.

INVALID characters
""""""""""""""""""

* :code:`$`

    * As we automatically append :code:`$` to the end of each line, you should
      not use this character.

* :code:`\\`

    * As we automatically escape any given expression, you should not explicitly
      escape your regular expression when declaring an :code:`ALL` marker.

:code:`REG`
"""""""""""

The :code:`REG` marker will tell the system to explicitly check for the given
regex which follows the marker.

:code:`RZD`
"""""""""""

The :code:`RZD` marker will tell the system to explicitly check for the given
string plus all possible TDL.

Anti whitelist
--------------

Don't like some of our rule(s)? UHBW allows you to specify a file, which contain
a list of rule(s) you don't want to be applied.

Simply use the :code:`--anti-whitelist` flag to provide one or more anti whitelist
files and UHBW will obey your wishes!


Understanding how UHBW whitelist works
--------------------------------------

If you have your own whitelist, with the following lines:

::

    facebook.com
    ALL .gov
    REG face
    RZD example

UHBW will do as follows:

* Remove every line which match :code:`facebook.com` and :code:`www.facebook.com`
* In complementary convert all lines with :code:`ALL` or :code:`REG` to the
  right format.
* Remove every line which match :code:`example.*`
* Check every line against the regular expression. More about this in next chapter.
* Print the results on screen or save to output file :code:`-o $output.file`.

The generated regular expression will from this example be:

::

    (\.gov$)|(face)|(example(.*))


.. note::
    The :code:`example` group is much longer, as we construct the list of TDL
    based on the Root Zone Database, of IANA and the Public Suffix List
    project.**

Which means UHBW actually will whitelist:

* all elements/lines which ends with :code:`.gov`
* all elements/lines which contain the word :code:`face`
* all possible TDL combination which starts with :code:`example`

File Formats
--------------

Your input files of domains / urls should be one domain / url per line and should also preferably be sorted.

::

    sort -u inputfile -o inputfile



Usage of the tool
-----------------

The script can be called by :code:`uhb-whitelist`, :code:`uhb_whitelist` or
:code:`ultimate-hosts-blacklist-whitelist`.

::

    usage: ultimate-hosts-blacklist-whitelist [-h]
                                                [-a ANTI_WHITELIST [ANTI_WHITELIST ...]]
                                                [--all ALL [ALL ...]] [-d] [-df]
                                                [-f FILE] [--hierachical-sorting]
                                                [-o OUTPUT] [-m] [--no-complement]
                                                [-p PROCESSES] [--reg REG [REG ...]]
                                                [--rzd RZD [RZD ...]]
                                                [--standard-sorting] [-v]
                                                [-w WHITELIST [WHITELIST ...]] [-wc]

    UHBW is a tool to clean up lists or hosts files with the hosted and/or your
    own whitelist.

    optional arguments:
        -h, --help            show this help message and exit
        -a ANTI_WHITELIST [ANTI_WHITELIST ...], --anti-whitelist ANTI_WHITELIST [ANTI_WHITELIST ...]
                                Read the given file override rules from the UHBW
                                hosted whitelist which is used by default. (See also
                                `-wc`)
        --all ALL [ALL ...]   Read the given file(s) and append its rules to the
                                whitelisting schema. Note: The rules injected
                                through this argument will be automatically prefixed
                                with the `ALL` marker.
        -d, --debug           Activate the debug mode. This mode will write the
                                whole processes to stdout.
        -df, --debug-into-file
                                Activate the logging into a file called
                                `uhb_whitelist_debug` at the current location.
        -f FILE, --file FILE  The file to whitelist/clean.
        --hierachical-sorting
                                Process a hierarchical sorting when outputing into a
                                file.
        -o OUTPUT, --output OUTPUT
                                Save the result to the given filename or path. (Can
                                not be the same as input file `-f`)
        -m, --multiprocessing
                                Activate the usage of multiple core processes.
        --no-complement       Forbid us the generation of complements while parsing
                                the whitelist list. Complements are `www.example.org`
                                if `example.org` is given and vice-versa.
        -p PROCESSES, --processes PROCESSES
                                The number of (maximal) processes core to use.
        --reg REG [REG ...]   Read the given file(s) and append its rules to the
                                whitelisting schema. Note: The rules injected
                                through this argument will be automatically prefixed
                                with the `REG` marker.
        --rzd RZD [RZD ...]   Read the given file(s) and append its rules to the
                                whitelisting schema. Note: The rules injected
                                through this argument will be automatically prefixed
                                with the `RZD` marker.
        --standard-sorting    Process a sorting when outputing into a file.
        -v, --version         Show the version end exist.
        -w WHITELIST [WHITELIST ...], --whitelist WHITELIST [WHITELIST ...]
                                Read the given file(s) and append its rules to the
                                whitelisting schema. Note: The rules injected
                                through this argument won't be changed. We follow what
                                you give us. That means that if you give any of our
                                supported rules, they will still be appended to the
                                whitelisting schema.
        -wc, --without-core   Disable the usage of the Ultimate Hosts Blacklist
                                whitelist hosted list.

    Crafted with ♥ by Nissar Chababy (Funilrys)

Contributors
------------

* Daniel - `@dnmTX`_
* Spirillen - `@spirillen`_

License
-------

::

    MIT License

    Copyright (c) 2018, 2019, 2020 Ultimate-Hosts-Blacklist
    Copyright (c) 2018, 2019, 2020 Nissar Chababy
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

.. _@dnmTX: https://github.com/dnmTX
.. _@spirillen: https://github.com/spirillen
.. _whitelist: https://github.com/Ultimate-Hosts-Blacklist/whitelist
.. _UHBW: https://github.com/Ultimate-Hosts-Blacklist/whitelist/tree/script
