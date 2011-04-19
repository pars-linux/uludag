
KDE 4 Applications
******************

A simple PyKDE KApplication
---------------------------

A basic example as follow::

    import sys

    from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
    from PyKDE4.kdeui import KApplication, KMainWindow

    from PyQt4.QtGui import QLabel, QWidget

    # A simple KMainWindow implementation
    class MainWindow(KMainWindow):
        def __init__(self):
            KMainWindow.__init__(self)

            self.resize(640, 480)
            label = QLabel("This is a simple PyKDE4 program", self)
            label.setGeometry(10, 10, 200, 20)

        def test(self):
            print "Test method called.."

    if __name__ == '__main__':

        # About data definitions
        appName     = "KApplication"
        catalog     = ""
        programName = ki18n("KApplication")
        version     = "1.0"
        description = ki18n("KApplication example")
        license     = KAboutData.License_GPL
        copyright   = ki18n("(c) 2009 Panthera Pardus")
        text        = ki18n("none")
        homePage    = "www.pardus.org.tr"
        bugEmail    = "info@pardus.org.tr"

        # Create about data from defined variables
        aboutData   = KAboutData(appName, catalog, programName, version, description,
                                    license, copyright, text, homePage, bugEmail)

        # Initialize Command Line arguments
        KCmdLineArgs.init(sys.argv, aboutData)

        # Create the application
        app = KApplication()

        # Create Main Window
        mainWindow = MainWindow()
        mainWindow.show()

        # Set top Widget as our mainWindow
        app.setTopWidget(mainWindow)

        # Run the app
        app.exec_()

If you need you can use ``QWidget`` instead of ``KMainWindow`` as top widget of app::

    class MainWindow(QWidget):
        def __init__(self):
            QWidget.__init__(self)

If you use ``QWidget`` you may need to define a connection for ``lastWindowClosed()`` signal::

    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

This application can run from command-line and you can use following cmd-line arguments::

    $ python kapp.py --help
    Usage: kapp.py [Qt-options] [KDE-options]

    KApplication example

    Generic options:
      --help                    Show help about options
      --help-qt                 Show Qt specific options
      --help-kde                Show KDE specific options
      --help-all                Show all options
      --author                  Show author information
      -v, --version             Show version information
      --license                 Show license information
      --                        End of options

For detailed information about ``KApplication`` you can grab api doc from [#]_. For example used above follow [#]_.

Running a KApplication from KDE4 System Settings
------------------------------------------------

To run a ``KApplication`` from System Settings you need a proper ``.desktop`` file installed under
``/usr/kde/4/share/kde4/services``.

Example ``.desktop`` file::

    [Desktop Entry]
    Exec=kcmshell4 service-manager
    Icon=preferences-desktop
    Type=Service
    X-KDE-ServiceTypes=KCModule

    X-KDE-Library=kpythonpluginfactory
    X-KDE-ParentApp=kcontrol
    X-KDE-PluginKeyword=service-manager/service-manager

    X-KDE-System-Settings-Parent-Category=computer-administration
    X-KDE-Weight=70

    Name=Service Manager
    Name[x-test]=xxService Managerxx
    Name[tr]=Servis Yöneticisi
    Comment=Service Manager
    X-KDE-Keywords=python service managers

The ``.desktop`` file above will add an entry for "Service Manager" under 
*Computer Administration* section in *System Settings* with ``preferences-desktop`` icon.
For above ``.desktop`` file you need to put "Service Manager" application under 
``/usr/kde/4/share/apps/service-manager`` and application name should be ``service-manager``.

Also for embedding a ``KApplication`` into *System Settings*, your application should have 
``CreatePlugin`` method::

    def CreatePlugin(widget_parent, parent, component_data):
        return ServiceManager(component_data, parent)

This method will call by *System Settings* and it should return a ``KCModule`` implementation like::

    class ServiceManager(KCModule):
        def __init__(self, component_data, parent):
            KCModule.__init__(self, component_data, parent)
            MainManager(self, standAlone=False)

``MainManager`` is your ``topWidget`` defined for ``KApplication``. 

.. tip:: If you need to use ``DBusQtMainLoop`` you must define it before creating the ``MainManager``.

.. rubric:: Footnotes
.. [#] http://api.kde.org/4.x-api/kdelibs-apidocs/kdeui/html/classKApplication.html
.. [#] http://svn.pardus.org.tr/uludag/branches/kde4-managers/tutorial


**Last Modified Date:** |today|

:Author: Gökmen Göksel

