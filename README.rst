URL checker
=======================

|PyPI| |GitHub-license| |Requires.io| |Travis|

    Built from `makenew/python-package <https://github.com/makenew/python-package>`__.

.. |PyPI| image:: https://img.shields.io/pypi/v/urlchecker.svg
   :target: https://pypi.python.org/pypi/urlchecker
   :alt: PyPI
.. |GitHub-license| image:: https://img.shields.io/github/license/Flaiming/urlchecker.svg
   :target: ./LICENSE.txt
   :alt: GitHub license
.. |Requires.io| image:: https://img.shields.io/requires/github/Flaiming/urlchecker.svg
   :target: https://requires.io/github/Flaiming/urlchecker/requirements/
   :alt: Requires.io
.. |Travis| image:: https://img.shields.io/travis/Flaiming/urlchecker.svg
   :target: https://travis-ci.org/Flaiming/urlchecker
   :alt: Travis

Description
-----------

Module for checking if given URLs are working and if so, if they are parking domains or not.

Installation
------------

This package is registered on the `Python Package Index (PyPI)`_
as urlchecker_.

Add this line to your application's requirements.txt

::

    urlchecker

and install it with

::

    $ pip install -r requirements.txt

If you are writing a Python package which will depend on this,
add this to your requirements in ``setup.py``.

Alternatively, install it directly using pip with

::

    $ pip install urlchecker

.. _urlchecker: https://pypi.python.org/pypi/urlchecker
.. _Python Package Index (PyPI): https://pypi.python.org/

Development and Testing
-----------------------

Source Code
~~~~~~~~~~~

The `urlchecker source`_ is hosted on GitHub.
Clone the project with

::

    $ git clone https://github.com/Flaiming/urlchecker.git

.. _urlchecker source: https://github.com/Flaiming/urlchecker

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

1. Fork it (https://github.com/Flaiming/urlchecker/fork).
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
