Gazu Publisher
==============

Tools to send previews to Kitsu from desktop enviromnents.

Setup development enviromnent
-----------------------------

.. code:: bash

    mkvirtualenv gazupublisher --python /usr/bin/python3
    pipenv install --dev
    add2virtualenv .
    python gazupublisher/__main__.py

Install Blender add-on
----------------------
A Blender add-on is given to link the interface and Blender. To set-up, please
follow these steps :

1. Find your path layout :
Blender uses a config folder (usually where all your add-ons are placed). If you
don't know where it is on your machine, see here :
https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html

2. Put the folder at the right place
Once you found this path, you must place the 'launch_kitsu.py' file in the
folder scripts/startup/ (it doesn't exist by default, you might have to create
it). The  link above can still be useful to find this directory.

3. Install dependencies
You may also need to install dependencies in order to make everything work. In
the folder "scripts/addons/modules" (that you might need to create too), you need
to have a folder gazu, a folder gazu_publisher, a folder qtazu and a file "Qt.py"



About authors
-------------

Gazu is written by CG Wire, a company based in France. We help small to
midsize CG studios to manage their production and build pipeline
efficiently.

We apply software craftmanship principles as much as possible. We love
coding and consider that strong quality and good developer experience
matter a lot. Our extensive knowledge allows studios to get better at
managing production and doing software. They can focus more on the artistic
work.

Visit `cg-wire.com <https://cg-wire.com>`__ for more information.

|CGWire Logo|

.. |CGWire Logo| image:: https://zou.cg-wire.com/cgwire.png
   :target: https://cg-wire.com
