Gazu Publisher
==============

Tools to send previews to Kitsu from desktop enviromnents.

Setup development enviromnent
-----------------------------
Disclaimer :

The following procedure intents to give easy steps to install the gazu publisher.

However, depending on your own local architecture, you might want to take
some liberties from this tutorial.
This tutorial details a procedure to :
    - Create a virtual environment
    - Install the gazu publisher inside this virtual environment
    - Setup the link file between the gazu publisher and your software
Please note that these steps can (must) be adapted to your own local
organisation regarding virtual environments, third-party packages, etc...

*Requirement : Make sure you have a zou instance running.*

Download pyqt-distutils ?
1. First, create a virtual environment associated to the software's Python executable.

    You can skip this step if you already have such a setup.

    You have to make sure this venv is linked to the correct Python interpreter
    depending on your software :


        - In Blender, the path of this interpreter can be found thanks to the internal variable **bpy.app.binary_path_python** (https://docs.blender.org/api/current/bpy.app.html#bpy.app.binary_path_python).


        - In Maya, the executable (named mayapy) can usually be found at "/usr/Autodesk/maya20xx/bin/mayapy" (https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/Maya/files/GUID-83799297-C629-48A8-BCE4-061D3F275215-htm.html)

    Once you found the path, create the virtual environment and activate it :

    .. code:: bash

        # Create the environment in the local directory
        virtualenv --python <your_python_exec_path> ./gazu_publisher
        # Activate it
        source gazu_publisher/bin/activate

    If you're using the package virtualenvwrapper, you can use :

    .. code:: bash

        mkvirtualenv --python <your_python_exec_path> gazu_publisher
        workon gazu_publisher

2. Install the gazu publisher through pip.

    Make sure the virtualenv you just created is activated. Then simply run :

    .. code:: bash

        pip install git+https://github.com/LedruRollin/gazu-publisher.git

    This will install the gazu publisher in the container associated to your virtual environment.

    For Blender users :
        The gazu publisher is an application based on the Qt library, and more precisely on its Qt bindings (PyQt/PySide).
        Since these bindings are not natively provided in Blender, you need to also download one of them in your virtual environment :

        .. code:: bash

            pip install PyQt5

        or

        .. code:: bash

            pip install PySide2



3. Link the gazu publisher to your software.

    Finally, we must indicate the gazu publisher location to the targeted software.
    To do so, we provide handlers that can make the bridge between the two parties.
    Please note you will have to modify these files to make sure everything works along your pipeline.

    - Blender :
        A Blender add-on is given to link the interface and Blender.
        This add-on makes three things :

        - It adds the path of the gazu publisher to the sys.path variable. To do that, you must manually set the 'gazupublisher_folder' variable at the beginning with the path of the project.
        - It makes work together the Qt and Blender event loops
        - It adds the adequate component to the Blender UI (Window > Launch Kitsu)

        After setting the path of the project, you must place the add-on with your other start-up files in the folder (https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html).

    - Maya :
        A Maya userSetup.py is provided, which makes two things :

        - It adds the path of the gazu publisher to the sys.path variable. To do that, you must manually set the 'gazupublisher_folder' variable at the beginning with the path of the project.
        - It adds the adequate component to the Maya UI

Troubleshooting
---------------
- gazupublisher.exceptions.TranslationException: Loading of the translation file at <path> failed
    The translation files are missing
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
