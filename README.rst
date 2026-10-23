Method Lines
============

.. image:: https://github.com/simpleigh/method-lines/actions/workflows/build.yml/badge.svg
   :alt: Build Status
   :target: https://github.com/simpleigh/method-lines/actions/workflows/build.yml

.. image:: https://img.shields.io/github/issues/simpleigh/method-lines.svg
   :alt: Issues
   :target: https://github.com/simpleigh/method-lines/issues

.. image:: https://img.shields.io/pypi/v/method-lines.svg
   :alt: Version
   :target: https://pypi.python.org/pypi/method-lines/

.. image:: https://img.shields.io/pypi/dm/method-lines.svg
   :alt: Downloads
   :target: https://pypi.python.org/pypi/method-lines/

.. image:: https://img.shields.io/pypi/pyversions/method-lines.svg
   :alt: Supported Python versions
   :target: https://pypi.python.org/pypi/method-lines/

.. image:: https://img.shields.io/pypi/status/method-lines.svg
   :alt: Development Status
   :target: https://pypi.python.org/pypi/method-lines/

.. image:: https://img.shields.io/pypi/format/method-lines.svg
   :alt: Download format
   :target: https://pypi.python.org/pypi/method-lines/

.. image:: https://img.shields.io/pypi/l/method-lines.svg
   :alt: Licence
   :target: https://pypi.python.org/pypi/method-lines/

Produces method lines and resources for peals in parts.

NOTE: This is very much work-in-progress with lots of spaghetti!

Usage
-----

1. **Install the Ringing Class Library**.

   You can download the latest source from
   `GitHub <https://github.com/ringing-lib/ringing-lib>`_.
   After obtaining appropriate prerequisites you can configure and install.
   Within the Ringing Class Library source tree:

   .. code-block:: bash

      make
      sudo make install

   This is needed to provide tools like ``gsiril`` and ``psline``.

2. **Install Using pip**

   Install directly from
   `PyPI <https://pypi.python.org/pypi/method-lines/>`_:

   .. code-block:: bash

      pip install method_lines

3. **Build an example**

   .. code-block:: bash

      method-lines all examples/major/smith

Development
-----------

Install `uv <https://docs.astral.sh/uv/>`_, then run::

   make sync
   make check
   make build
