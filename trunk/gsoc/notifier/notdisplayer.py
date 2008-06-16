#!/usr/bin/python
    
# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext
    
# Import header that specifies notification class
from notification import *

# Import PyQt4 GUI stuff:
from PyQt4 import QtCore, QtGui, uic

class NotificationTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, notification_displayer, icon = None, parent = None):
        if icon == None:
            QtGui.QSystemTrayIcon.__init__(self, parent)
        else:
            QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.BuildMenu()
        self.show()
        self.notification_displayer = notification_displayer
    
    def Die(self):
        quit()
    
    def BuildMenu(self):
        self.menu = QtGui.QMenu()
        self.action = QtGui.QAction(_("Exit"), self.menu)
        self.menu.addAction(self.action)
        self.connect(self.action,  QtCore.SIGNAL("triggered()"),  self.Die)
        self.setContextMenu(self.menu)
    
    def DisplayNotification(self, notif):
        if isinstance(notif,  Notification) == True:
            self.showMessage(_("Notification arrived!"),  notif.text)
        else:
            self.showMessage(_("Error"),  _("Typing error, this program has just bought the farm."))
                    
class NotificationDisplayer:
    def __init__(self):
        self.tray_icon = NotificationTrayIcon(self,  QtGui.QIcon("./icons/icon.png"))
        self.notification_windows = {}
        self.nexthandle = 0
        self.Configure()
    
    def Configure(self):
		# Configurations:
		
		# Load the GUI:
		self.ui_class, self.base_class = uic.loadUiType("ui/default_notif_window.ui")
		self.default_GUI_used = True
		self.NotificationWindowClass = self.MakeNotificationWindowClass()
		
		# Configure notification window geometry:
		screen = QtGui.QDesktopWidget().screenGeometry()
		self.percent_width = 17
		self.percent_height = 13
		self.pixel_width = self.percent_width * screen.width() / 100
		self.pixel_height = self.percent_height * screen.height() / 100
		
		# Configure starting position:
		# self.starting = "lowerRight"
		self.starting = "upperRight"
		# self.starting = "manual"
		
		# Manual starting position:
		self.start_x = 300
		self.start_y = 500
		
		# Configure growth direction:
		# self.direction = "up"
		self.direction = "down"  
		
		# Configure animation timing (milliseconds):
		self.total_animation_time = 500
		self.time_quanta = 18
		
		# Configure the lifetime of the notification windows:
		self.lifetime = 5500

    def ChangeLayout(self):
    	# Move all currently open notification windows properly:
    	handle_list = self.notification_windows.keys()
    	handle_list.sort()
    	for handle in handle_list:
			dest_x, dest_y, lw_x, lw_y = self.notification_windows[handle].CalculateDestination()
			self.notification_windows[handle].MoveAnimated(dest_x, dest_y)
    
    def DisplayNotification(self, notif):
    	# We dont want any caption or border on our notification displayer window:
		window_flags = QtCore.Qt.WindowFlags() | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowStaysOnTopHint
    	# Create a new notification window to display the incoming notification and
    	# append the new notification window to the list of currently open notification windows:
		self.notification_windows[self.nexthandle] = self.NotificationWindowClass(displayer = self, handle = self.nexthandle, percent_width = self.percent_width, percent_height = self.percent_height, parent = None, window_flags = window_flags)
		# Attach the changeLayout signal to the corresponding method:
		QtCore.QObject.connect(self.notification_windows[self.nexthandle], QtCore.SIGNAL("changeLayout()"), self.ChangeLayout)		
		# Show the window:
		self.notification_windows[self.nexthandle].ShowNotification(notif)
		self.nexthandle = self.nexthandle + 1
		
    def MakeNotificationWindowClass(self_outer):
		class NotificationWindow(self_outer.ui_class, self_outer.base_class):
			def __init__(self, displayer, handle, percent_width, percent_height, parent = None, window_flags = 0):
				# Set up the UI read from the .ui file:
				self_outer.ui_class.__init__(self)
				self_outer.base_class.__init__(self, parent, window_flags)
				
				self.setupUi(self)
				
				# Store the handle of this window:
				self.handle = handle
				self.displayer = displayer
				
				# Calculate the preferred notification window size in pixels (from percentages given)
				screen = QtGui.QDesktopWidget().screenGeometry()
				self.maxWidth = screen.width() * percent_width / 100
				self.preferred_height = screen.height() * percent_height / 100
				
				# Set initial conditions of animation state variables:
				self.timer = QtCore.QTimer()
				self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.MoveAnimatedHelper)
				self.currenty_animating = False
				self.destination_x = 0
				self.destination_y = 0
				self.step_size_x = 0
				self.step_size_y = 0
				
				# Set some properties of the default GUI:
				if self_outer.default_GUI_used == True:
					self.vboxlayout.setAlignment(QtCore.Qt.AlignTop)
					self.exit_button.setIcon(QtGui.QIcon("./icons/exit.png"))
				
				# Set some properties of the GUI (skin-independent):
				
				# Minimum / Maximum size of the window:
				self.setMinimumSize(QtCore.QSize(self.maxWidth, self.preferred_height))
				self.setMaximumSize(QtCore.QSize(self.maxWidth, 2 * self.preferred_height))
				
				# Maximum sizes of the mandatory components:
				self.notification_picture.setMaximumSize(QtCore.QSize(self.maxWidth * 0.2, self.preferred_height * 0.3))
				self.notification_title.setMaximumSize(QtCore.QSize(self.maxWidth * 0.6, self.preferred_height * 0.3))
				self.notification_text.setMaximumSize(QtCore.QSize(self.maxWidth * 0.95, self.preferred_height * 1.7)) 
				
				# Attach remaining signals:
				QtCore.QObject.connect(self.exit_button, QtCore.SIGNAL("clicked()"), self.Destroy)	
				
			def ShowNotification(self, notification):
				# Set the text of the notification window to reflect the incoming notification:
				self.notification_title.setText(notification.notification_title)
				self.notification_text.setText(notification.notification_text)
				self.notification_picture.setPixmap(QtGui.QPixmap(notification.notification_icon_path))
				# Make sure that the window height does not exceed 2 times the preferred size:
				hinted_size = self.sizeHint()
				if hinted_size.height() < self.preferred_height:
					self.resize(self.maxWidth, self.preferred_height)
				elif hinted_size.height() < 2 * self.preferred_height:
					self.resize(self.maxWidth, hinted_size.height())
				else:
					self.resize(self.maxWidth, 2 * self.preferred_height)
				# Move the new notification window to a suitable place:
				dest_x, dest_y, lw_x, lw_y  = self.CalculateDestination()
				self.MoveImmediately(lw_x, lw_y)
				self.MoveAnimated(dest_x, dest_y)
				self.show()
				# Set up the timer to make sure that the window dies when its lifetime is over:
				QtCore.QTimer().singleShot(self.displayer.lifetime, self.Destroy)
				
			def Destroy(self):
				self.displayer.notification_windows.pop(self.handle)
				self.deleteLater()
				self.emit(QtCore.SIGNAL("changeLayout()"))
				
			def CalculateDestination(self):
				dest_x = 0
				dest_y = 0
				lw_x = 0
				lw_y = 0
				other_handles = self.displayer.notification_windows.keys()
				other_handles.sort()
				other_handles = other_handles[:other_handles.index(self.handle)]
				
				screen = QtGui.QDesktopWidget().availableGeometry()
				
				if other_handles == []:
					if self.displayer.starting == "manual":
						dest_x = screen.x() + self.displayer.start_x
						dest_y = screen.y() + self.displayer.start_y
					elif self.displayer.starting == "upperRight":
						dest_x = screen.x() + screen.width() - self.width()
						dest_y = screen.y()
					elif self.displayer.starting == "lowerRight":
						dest_x = screen.x() + screen.width() - self.width()
						dest_y = screen.y() + screen.height() - self.height()
						
					lw_x = dest_x
					lw_y = dest_y	
				else:
					last_window_handle = other_handles[-1]
					last_window = self.displayer.notification_windows[last_window_handle]
				
					if self.displayer.direction == "up":
						dest_x = last_window.destination_x
						dest_y = last_window.destination_y - self.height()
					elif self.displayer.direction == "down":
						dest_x = last_window.destination_x
						dest_y = last_window.destination_y + last_window.height()
						
					lw_x = last_window.x()
					lw_y = last_window.y()
				
				return (dest_x, dest_y, lw_x, lw_y)
				
			def MoveImmediately(self, destination_x, destination_y):
				self.destination_x = destination_x
				self.destination_y = destination_y
				self.move(destination_x, destination_y)
				
			def MoveAnimated(self, destination_x, destination_y):
				# Calculate the animation speed etc:
				self.destination_x = destination_x
				self.destination_y = destination_y
				
				diff_x = destination_x - self.x()
				diff_y = destination_y - self.y()
				self.step_size_x = diff_x * self.displayer.time_quanta / self.displayer.total_animation_time
				self.step_size_y = diff_y * self.displayer.time_quanta / self.displayer.total_animation_time
				
				self.currently_animating = True

				self.timer.start(self.displayer.time_quanta)
				
			def MoveAnimatedHelper(self):
				# Move the window one step at each quanta:
				self.move(self.x() + self.step_size_x, self.y() + self.step_size_y)
				# If we arrived at the destination, stop animation:
				if abs(self.x() - self.destination_x) < abs(self.step_size_x) or abs(self.y() - self.destination_y) < abs(self.step_size_y):
					self.timer.stop()
					self.currently_animating = False
					self.move(self.destination_x, self.destination_y)
					
		return NotificationWindow
