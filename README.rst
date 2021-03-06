URL checker
=======================

|GitHub-license| |Requires.io| |Travis|

    Built from `makenew/python-package <https://github.com/makenew/python-package>`__.

.. |GitHub-license| image:: https://img.shields.io/github/license/flaiming/urlchecker.svg
   :target: ./LICENSE.txt
   :alt: GitHub license
.. |Requires.io| image:: https://requires.io/github/flaiming/urlchecker/requirements.svg?branch=master
     :target: https://requires.io/github/flaiming/urlchecker/requirements/?branch=master
     :alt: Requirements Status
.. |Travis| image:: https://img.shields.io/travis/flaiming/urlchecker.svg?branch=master
   :target: https://travis-ci.org/flaiming/urlchecker
   :alt: Travis
.. image:: https://coveralls.io/repos/github/flaiming/urlchecker/badge.svg?branch=master 
   :target: https://coveralls.io/github/flaiming/urlchecker?branch=master 
   :alt: Coveralls

Description
-----------

Module for checking if given URLs are working and if so, if they are parking domains or not.

Installation
------------

This package is currently in development and available only through git.

Development and Testing
-----------------------

Source Code
~~~~~~~~~~~

The `urlchecker source`_ is hosted on GitHub.
Clone the project with

::

    $ git clone https://github.com/flaiming/urlchecker.git

.. _urlchecker source: https://github.com/flaiming/urlchecker

Requirements
~~~~~~~~~~~~

You will need `Python 3`_ with pip_.

Install the development dependencies with

::

    $ pip install -r requirements.devel.txt

.. _pip: https://pip.pypa.io/
.. _Python 3: https://www.python.org/

Tests
~~~~~

Lint code with

::

    $ python setup.py lint


Run tests with

::

    $ python setup.py test

Contributing
------------

Please submit and comment on bug reports and feature requests.

To submit a patch:

1. Fork it (https://github.com/flaiming/urlchecker/fork).
2. Create your feature branch (``git checkout -b my-new-feature``).
3. Make changes. Write and run tests.
4. Commit your changes (``git commit -am 'Add some feature'``).
5. Push to the branch (``git push origin my-new-feature``).
6. Create a new Pull Request.

License
-------

This Python package is licensed under the MIT license.

Warranty
--------

This software is provided "as is" and without any express or implied
warranties, including, without limitation, the implied warranties of
merchantibility and fitness for a particular purpose.
