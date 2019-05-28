The Ultimate Hosts Blacklist whitelist script
=============================================

This is the branch which contain the script which we use to whitelist domains or IP into our infrastructure.

Installation
------------

::

    $ pip3 install --user ultimate-hosts-blacklist-whitelist



Complementary whitelist
-----------------------

Our script allow us to link one or more file(s) to the system which will be used in complementary of our whitelist list.

Special markers
---------------

If you already used a whitelist list you already know that we generaly only list all domains we want to whitelist one by one.

It's also possible to do that with our whitelisting system but we can do more.

:code:`ALL`
^^^^^^^^^^^

The :code:`ALL` marker will tell the system to escape and regex check againt what follows.

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
* Check every line again the regular expression.
* Print or save on screen the results.

The generated regular expression will be in this example:

::

    (\.gov$)|(face)|(example(.*))


**NOTE: The :code:`example` group is much longer as we construct the list of TDL based on the Root Zone Database of the IANA and the Public Suffix List project.**

Which actually means that we whitelist:

* all elements/lines which ends with :code:`.gov`
* all elements/lines which contain the word :code:`face`

Contributors
------------

* Daniel - `@dnmTX`_

Usage of the script
-------------------

The sript can be called as :code:`uhb-whitelist`, :code:`uhb_whitelist` and :code:`ultimate-hosts-blacklist-whitelist`.

::

    usage: uhb_whitelist [-h] [-d] [-f FILE] [-o OUTPUT] [-m] [-p PROCESSES] [-v]
                        [-w WHITELIST [WHITELIST ...]] [-wc]

    The tool to clean a list or a hosts file with the Ultimate Hosts Blacklist
    whitelist list or your own.

    optional arguments:
        -h, --help            show this help message and exit
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


.. _@dnmTX: https://github.com/dnmTX