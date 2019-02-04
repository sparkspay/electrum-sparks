Electrum-SPARKS - Lightweight Sparkspay client
=====================================

::

  Licence: MIT Licence
  Author: Thomas Voegtlin
  Language: Python
  Homepage: https://electrum.sparkscoin.io/


.. image:: https://travis-ci.org/akhavr/electrum-sparks.svg?branch=master
    :target: https://travis-ci.org/akhavr/electrum-sparks
    :alt: Build Status





Getting started
===============

Electrum-SPARKS is a pure python application. If you want to use the
Qt interface, install the Qt dependencies::

    sudo apt-get install python3-pyqt5

If you downloaded the official package (tar.gz), you can run
Electrum-SPARKS from its root directory, without installing it on your
system; all the python dependencies are included in the 'packages'
directory (except neoscrypt).

To install neoscrypt dependency in the 'packages' dir run once by hand::

    sudo python3 ./lib/neoscrypt_module/setup.py install

To run Electrum-SPARKS from its root directory, just do::

    ./electrum-sparks

You can also install Electrum-SPARKS on your system, by running this command::

    sudo apt-get install python3-setuptools
    pip3 install .[fast]

This will download and install the Python dependencies used by
Electrum-SPARKS, instead of using the 'packages' directory.
The 'fast' extra contains some optional dependencies that we think
are often useful but they are not strictly needed.

If you cloned the git repository, you need to compile extra files
before you can run Electrum-SPARKS. Read the next section, "Development
Version".



Development version
===================

Check out the code from GitHub::

    git clone https://github.com/SparksReborn/electrum-sparks.git
    cd electrum-sparks

Run install (this should install dependencies)::

    pip3 install .[fast]

Render the SVG icons to PNGs (optional)::

    for i in lock unlock confirmed status_lagging status_disconnected status_connected_proxy status_connected status_waiting preferences; do convert -background none icons/$i.svg icons/$i.png; done

Compile the icons file for Qt::

    sudo apt-get install pyqt5-dev-tools
    pyrcc5 icons.qrc -o gui/qt/icons_rc.py

Compile the protobuf description file::

    sudo apt-get install protobuf-compiler
    protoc --proto_path=lib/ --python_out=lib/ lib/paymentrequest.proto

Create translations (optional)::

    sudo apt-get install python-requests gettext
    ./contrib/make_locale




Creating Binaries
=================


To create binaries, create the 'packages' directory::

    ./contrib/make_packages

This directory contains the python dependencies used by Electrum-SPARKS.

Android
-------

See `gui/kivy/Readme.txt` file.
