
Plasmoids
*********

Hello World Plasmoid with using Widgets
---------------------------------------

.. seealso:: 
    http://techbase.kde.org/Development/Tutorials/Plasma/Python/GettingStarted

A plasma package tree looks like::

    $ tree hello-world/
    hello-world/
    |-- contents
    |   `-- code
    |       `-- main.py
    `-- metadata.desktop

``contents`` may include ``ui`` directory if you need but ``code`` directory 
and ``metadata.desktop`` file is mandatory. For yet another *Hello World* example ``metadata.desktop`` looks like::

    [Desktop Entry]
    Encoding=UTF-8
    Name=Hello World
    Name[tr]=Merhaba Dünya
    Name[x-test]=xxHello Worldxx
    Type=Service
    ServiceTypes=Plasma/Applet
    X-Plasma-API=python
    X-Plasma-MainScript=code/main.py
    Icon=applications-toys

    X-KDE-PluginInfo-Author=Panthera Pardus
    X-KDE-PluginInfo-Email=info@pardus.org.tr
    X-KDE-PluginInfo-Name=hello-world
    X-KDE-PluginInfo-Version=1.0
    X-KDE-PluginInfo-Website=http://www.pardus.org.tr
    X-KDE-PluginInfo-Category=Utilities
    X-KDE-PluginInfo-Depends=
    X-KDE-PluginInfo-License=GPL
    X-KDE-PluginInfo-EnabledByDefault=true

.. tip:: For more information about ``X-KDE-PluginInfo-Category`` you may visit [#]_

``X-Plasma-MainScript`` shows main plasmoid file, this file must have a ``CreateApplet`` method like::

    def CreateApplet(parent):
        return HelloWorldApplet(parent)


which returns a ``plasmascript.Applet`` from ``PyKDE4.Plasma`` and this applet may produce like::

    # Plasma Libs
    from PyKDE4.plasma import Plasma
    from PyKDE4 import plasmascript

    # Qt Core
    from PyQt4.Qt import Qt, QGraphicsLinearLayout

    class HelloWorldApplet(plasmascript.Applet):
        """ Our main applet derived from plasmascript.Applet """

        def __init__(self, parent, args=None):
            plasmascript.Applet.__init__(self, parent)

        def init(self):
            """ Const method for initializing the applet """

            # Configuration interface support comes with plasma
            self.setHasConfigurationInterface(False)

            # Aspect ratio defined in Plasma
            self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

            # Theme is a const variable holds Applet Theme
            self.theme = Plasma.Svg(self)

            # It gets default plasma theme's background
            self.theme.setImagePath("widgets/background")

            # Resize current theme as applet size
            self.theme.resize(self.size())

            # Update the size of Plasmoid
            self.constraintsEvent(Plasma.SizeConstraint)

            # We need a layout
            self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
            self.setLayout(self.layout)

            # A label
            self.label = Plasma.Label(self.applet)

            # to say hello world !
            self.label.setText("Hello World !")

            # and centered
            self.label.setAlignment(Qt.AlignCenter)

            # add it to current layout
            self.layout.addItem(self.label)

            # resize the applet
            self.resize(125, 125)

        def constraintsEvent(self, constraints):
            if constraints & Plasma.SizeConstraint:
                self.theme.resize(self.size())

    def CreateApplet(parent):
        return HelloWorldApplet(parent)

Installing a Plasmoid
---------------------

.. tip:: You can check-out the above example from [#]_

Plasma applets can be packaged in zip files and installed using the ``plasmapkg`` command line tool. 
The directory structure which we have used for our project matches that need in the zip file. 
All we have to do is zip it update. Run the following command from inside the hello-world directory::

    $ zip -r ../hello-world.zip .

This will create the hello-world.zip file in the directory just above the hello-world directory. 
Go to this directory in the shell and run this ``plasmapkg`` command to install our little hello-world applet::

    $ plasmapkg -i hello-world.zip

This installs the applet into your home directory. Now we can run it. When developing applets it is more 
convenient to use the ``plasmoidviewer``. This is a little utility which displays an applet in a window instead
of you having to use your desktop. This command below will run our applet::

    $ plasmoidviewer hello-world

To uninstall our applet we use ``plasmapkg`` again with its ``-r`` option::

    $ plasmapkg -r hello-world

.. tip:: Instead of these steps you may use [#]_ ``mkplasma hello-world`` (not in directory)

.. rubric:: Footnotes
.. [#] http://techbase.kde.org/Projects/Plasma/PIG
.. [#] http://svn.pardus.org.tr/uludag/trunk/kde4/tutorial/hello-world
.. [#] http://svn.pardus.org.tr/uludag/trunk/kde4/service-manager/plasmoid/systemservices/contents/code/mkplasma

**Last Modified Date:** |today|

:Author: Gökmen Göksel

