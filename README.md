# PyClutter

Clutter is a toolkit for creating compelling, dynamic, and portable graphical
user interfaces. Clutter is free software, developed by the GNOME community.

PyClutter provides various overrides for the Clutter introspection data
and PyGObject that can be used to improve the API coverage of the pure
introspection-based Clutter module, as well as make the API more Pythonic.

## Requirements

  * PyGObject 3.0 or higher
  * Python 2.7 or higher
  * Clutter introspection data

## Installing PyClutter

In order to install this module type the following:

    $ ./configure
    $ make
    # make install

To avoid installing to a system directory you can change the installation
prefix at configure time with:

    $ ./configure --prefix=/some/other/place

## Using Clutter from Python

Just import the module using:

    from gi.repository import Clutter

And that's it.

## Documentation and API reference

The Python API available through introspection is documented here:

    http://lazka.github.io/pgi-docs/Clutter-1.0/

The canonical reference for the C API is available here:

    https://developer.gnome.org/clutter/

## Copyright and License

This library is free software; you can redistribute it and/or modify it under
the terms of the GNU Library General Public License as published by the Free
Software Foundation; either version 2.1 of the License, or (at your option)
any later version

This library is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Library General Public License for more
details.

You should have received a copy of the GNU Library General Public License along
with this library. If not, see http://www.gnu.org/licenses/. 
