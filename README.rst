Gazu Publisher
==============

Tools to send previews to Kitsu from desktop enviromnents.

|Build badge| 

Setup development enviromnent
-----------------------------
Disclaimer :

The following procedure intents to give easy steps to install the gazu publisher.

However, depending on your own local architecture, you might want to take
some liberties from this tutorial, which details a procedure to :

- Create a virtual environment
- Install the gazu publisher inside this virtual environment
- Setup the link file between the gazu publisher and your software

Please note that these steps can (must) be adapted to your own local
organisation regarding virtual environments, third-party packages, etc...

*Requirement : Make sure you have a zou instance running.*

1. First, create a virtual environment associated to the software's Python executable.

    To make sure we don't mess with any of your own Python packages, we propose you here to install a virtual environment.
    You can skip this step if you already have such a setup.

    A virtual environment is a box that isolates your packages to make sure they work well together
    To create it, we have to make sure that this virtual environment is linked to the correct Python interpreter used by your software.
    Let's find the Python executable that your software is using :


        - In Blender, the path of this interpreter can be found thanks to the internal variable **bpy.app.binary_path_python** (https://docs.blender.org/api/current/bpy.app.html#bpy.app.binary_path_python).

            .. image:: ./gifs/find_blender_exec.gif

        - In Maya, the executable (named mayapy) can usually be found at "/usr/Autodesk/maya20xx/bin/mayapy" (https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/Maya/files/GUID-83799297-C629-48A8-BCE4-061D3F275215-htm.html)

    Once you found the path, we can create the virtual environment and activate it :

    .. code:: bash

        # Create the environment in the local directory
        virtualenv --python <the_python_exec_path_we_just_found> <directory_where_you_want_to_install>
        # Activate it
        source gazu_publisher/bin/activate

    Note that if you're using the package virtualenvwrapper, you can also use :

    .. code:: bash

        mkvirtualenv --python <the_python_exec_path_we_just_found> gazu_publisher
        workon gazu_publisher

2. Install the gazu publisher through pip.

    Make sure the virtualenv you just created is activated (its name should appear before your command line).
    Then simply run :

    .. code:: bash

        pip install git+https://github.com/LedruRollin/gazu-publisher.git

    This will install the gazu publisher inside your virtual environment.
    You can use the command pip show to check the code was installed at the right place :

    .. code:: bash

        pip show gazupublisher

    For Blender users :
        The gazu publisher is an application based on the Qt library, and more precisely on its Python bindings (PyQt/PySide).
        Since these bindings are not natively provided in Blender, you need to also download one of them in your virtual environment :

        .. code:: bash

            pip install PyQt5

        or

        .. code:: bash

            pip install PySide2



3. Link the gazu publisher to your software.

    Finally, we must indicate the gazu publisher location to your software.
    To do so, we provide handlers that can make the bridge between the two sides.
    Please note that you may want to modify the file even beyond the scope of this tutorial.
    You'll find the file you want (depending on your software) in the folder 'gazupublisher/software_link' :

    - Blender :
        A Blender add-on is given to link the interface and Blender.
        This add-on makes three things :

        - It adds the path of the gazu publisher to the sys.path variable.
        - It makes work together the Qt and Blender event loops
        - It adds the adequate component to the Blender UI (Window > Launch Kitsu)

        To complete the file, you must manually set the 'gazupublisher_folder' variable at the beginning of the file with the path of the project.
        You can also set in this file the variable 'kitsu_host' with the URL of your instance of Kitsu, so that users won't have to fill it every time.
        After setting the path of the project, you must place the add-on with your other start-up files in the associated folder (https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html).
    - Maya :
        A Maya userSetup.py is provided, which makes two things :

        - It adds the path of the gazu publisher to the sys.path variable.
        - It adds the adequate component to the Maya UI

        To complete the file, you must manually set the 'gazupublisher_folder' variable at the beginning of the file with the path of the project.
        If you don't know where you put it, the command pip show can help you :

        .. code:: bash

            pip show gazupublisher

        You can also set in this file the variable 'kitsu_host', with the URL of your instance of Kitsu, so that users won't have to fill it every time.
        Once it's done, simply put the file in the Maya start-up directory. If you don't know where it is, it can be found like this :

        .. image:: ./gifs/find_maya_startup_dir.gif

        If you already have a userSetup.py, you can merge them.

Standalone mode
---------------

The application can be launched in standalone mode.
To do so, go to the code (installed into your virtualenv, use 'pip show gazupublisher' to see the path), and simply launch the main file in the gazupublisher folder.
Since it's not installed by default, Maya users need to install PySide2 or PyQt5 in their virtual environment to make things work.

Troubleshooting
---------------

If you're on Ubuntu/Debian and you encounter any bug on Maya regarding a failed ssl import, this may be caused by Maya itself.
If then you observe a problem (for example missing libssl and libcrypto librairies) when launching this command :

.. code:: bash

    ldd /usr/autodesk/maya2019/lib/python2.7/lib-dynload/_ssl.so

Then please check the folder /usr/autodesk/maya2019/support/python/2.7.11 and follow the instructions given by Maya.
If that last path leads to nowhere, you can try to find it with "locate ubuntu_ssl.so"

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

.. |Build badge| image:: https://travis-ci.org/cgwire/gazu-publisher.svg?branch=master
   :target: https://travis-ci.org/cgwire/gazu-publisher
.. |CGWire Logo| image:: https://zou.cg-wire.com/cgwire.png
   :target: https://cg-wire.com
