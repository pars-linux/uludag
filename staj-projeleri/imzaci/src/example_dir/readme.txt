Welcome to Wink

This version has been tested in Windows98, ME, 2000, XP and various distributions of Linux including Ubuntu, Fedora and Mandrake.

Two tutorial projects are present in this distribution. Once installed, run Wink and choose menu "Help > View tutorial 1". This will ask if you want to render now, choose yes. You will be shown the tutorial soon after the rendering is done.

The sample projects are named "tutorial.wnk" and "sample.wnk". These files are present in the Wink\Samples folder.

For more documentation, view the "Wink User Guide" in the Wink\Docs folder.


Installating Wink in Linux:
---------------------------

Run the "installer.sh" shell script in the command prompt and it will prompt you for the path to install Wink. The default path should be fine but if you want to have other users also use Wink you can specify a system wide directory such as "/bin/wink".

The installer does not create any shortcuts to the Wink executable, if you want shortcuts you will have to create them on your own depending on which window manager you use.


Known issues in the Linux version:
----------------------------------

1) The keyboard shortcuts and dialogs does not meet the UI guidelines for linux apps, it is more like a windows app. This is because Wink is ported from windows to linux and will be fixed in a later version.

2) The capture hotkeys may not work when a menu is open in any application because the window manager takes control of the keyboard and wink does not receive the events. As a workaround you can start timed capture just before opening the menu and keep it capturing shots as you open the menu and click on the menu item, then stop timed capture.


Happy winking ;)
Satish
http://www.debugmode.com/