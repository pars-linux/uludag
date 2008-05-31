#!/usr/bin/python
    
# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext
    
# Import header that specifies notification class
from notification import *

# Import PyQt4 GUI stuff:
from PyQt4 import QtCore, QtGui

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
            
class NotificationWindow(QtGui.QFrame):
	def __init__(self, displayer, handle, percent_width, percent_height, parent = None, window_flags = 0):
		QtGui.QFrame.__init__(self, parent, window_flags)
		
		# Store the handle of this window:
		self.handle = handle
		self.displayer = displayer
		
		# Calculate the preferred notification window size in pixels (from percentages given)
		screen = QtGui.QDesktopWidget().screenGeometry()
		self.maxWidth = screen.width() * percent_width / 100
		self.preferred_height = screen.height() * percent_height / 100
		
		# Configure main notification window:
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		self.setSizePolicy(sizePolicy)    	
		self.setObjectName("mainwindow")
		self.setMinimumSize(QtCore.QSize(self.maxWidth, self.preferred_height))
		self.setMaximumSize(QtCore.QSize(self.maxWidth, 2 * self.preferred_height))
		self.setFrameShape(QtGui.QFrame.StyledPanel)
		self.setFrameShadow(QtGui.QFrame.Raised)
		self.mainwindow_gridlayout = QtGui.QGridLayout(self)
		self.mainwindow_gridlayout.setObjectName("mainwindow_gridlayout")
		
		# Upper progress bar:
		self.progressBar_upper = QtGui.QProgressBar(self)
		self.progressBar_upper.setMaximumSize(QtCore.QSize(16777215, 5))
		self.progressBar_upper.setMaximum(0)
		self.progressBar_upper.setProperty("value", QtCore.QVariant(-1))
		self.progressBar_upper.setTextVisible(False)
		self.progressBar_upper.setInvertedAppearance(False)
		self.progressBar_upper.setObjectName("progressBar_upper")
		self.mainwindow_gridlayout.addWidget(self.progressBar_upper, 0, 0, 1, 1)

		# Horizontal box layout enclosing notification icon, notification title and close button:
		self.title_hboxlayout = QtGui.QHBoxLayout()
		self.title_hboxlayout.setObjectName("title_hboxlayout")
		
		# Notification icon:
		self.notification_picture = QtGui.QLabel(self)
		# Limit the size of the notification icon label:
		self.notification_picture.setMaximumSize(QtCore.QSize(self.maxWidth * 0.2, 16777215))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHeightForWidth(self.notification_picture.sizePolicy().hasHeightForWidth())
		self.notification_picture.setSizePolicy(sizePolicy)
		self.notification_picture.setPixmap(QtGui.QPixmap("notif.png"))
		self.notification_picture.setScaledContents(False)
		self.notification_picture.setObjectName("notification_picture")
		self.title_hboxlayout.addWidget(self.notification_picture)

		# Notification title label:
		self.notification_title = QtGui.QLabel(self)
		# Limit the size of the notification title label:
		self.notification_title.setMaximumSize(QtCore.QSize(self.maxWidth * 0.6, 16777215))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHeightForWidth(self.notification_title.sizePolicy().hasHeightForWidth())
		self.notification_title.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setFamily("UnBom")
		font.setPointSize(9)
		self.notification_title.setFont(font)
		self.notification_title.setWordWrap(True)
		self.notification_title.setObjectName("notification_title")
		self.notification_title.setText("Notification arrived!")		
		self.title_hboxlayout.addWidget(self.notification_title)
		
		# Vertical box layout used for aligning the exit button vertically:
		self.title_vboxlayout = QtGui.QVBoxLayout()
		self.title_vboxlayout.setObjectName("title_vboxlayout")
		
		# Exit button:
		self.exit_button = QtGui.QToolButton(self)
		self.exit_button.setIcon(QtGui.QIcon("exit.png"))
		self.exit_button.setObjectName("exit_button")
		# Attach the triggering signal of this button to the method Close:
		QtCore.QObject.connect(self.exit_button, QtCore.SIGNAL("clicked()"), self.Destroy)
		
		self.title_vboxlayout.addWidget(self.exit_button)
		self.title_vboxlayout.addStretch(1)
		
		self.title_hboxlayout.addLayout(self.title_vboxlayout)
		self.mainwindow_gridlayout.addLayout(self.title_hboxlayout, 1, 0, 1, 1)		
		
		# Lower progress bar:
		self.progressBar_lower = QtGui.QProgressBar(self)
		self.progressBar_lower.setMaximumSize(QtCore.QSize(16777215, 5))
		self.progressBar_lower.setMaximum(0)
		self.progressBar_lower.setProperty("value", QtCore.QVariant(-1))
		self.progressBar_lower.setTextVisible(False)
		self.progressBar_lower.setObjectName("progressBar_lower")
		self.mainwindow_gridlayout.addWidget(self.progressBar_lower, 2, 0, 1, 1)

		# Configure the inner frame:
		self.inner_frame = QtGui.QFrame(self)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHeightForWidth(self.inner_frame.sizePolicy().hasHeightForWidth())
		self.inner_frame.setSizePolicy(sizePolicy)
		self.inner_frame.setFrameShape(QtGui.QFrame.StyledPanel)
		self.inner_frame.setFrameShadow(QtGui.QFrame.Raised)
		self.inner_frame.setObjectName("inner_frame")
		self.inner_frame_gridlayout = QtGui.QGridLayout(self.inner_frame)
		self.inner_frame_gridlayout.setObjectName("inner_frame_gridlayout")

		# Configure the label that displays the actual notification message:
		self.notification_text = QtGui.QLabel(self.inner_frame)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHeightForWidth(self.notification_text.sizePolicy().hasHeightForWidth())
		self.notification_text.setSizePolicy(sizePolicy)  
		font = QtGui.QFont()
		font.setFamily("UnGraphic")
		self.notification_text.setFont(font)
		self.notification_text.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
		self.notification_text.setObjectName("notification_text")
		self.notification_text.setWordWrap(True)
		self.notification_text.setTextFormat(QtCore.Qt.AutoText)
		self.notification_text.setMinimumSize(QtCore.QSize(0, 0))
		self.notification_text.setMaximumSize(QtCore.QSize(self.maxWidth * 0.95, 16777215)) 
		
		self.inner_frame_gridlayout.addWidget(self.notification_text, 0, 0, 1, 1)
		self.mainwindow_gridlayout.addWidget(self.inner_frame, 3, 0, 1, 1)
		
		# Set animation parameters:
		self.timer = QtCore.QTimer()
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.MoveAnimatedHelper)
		self.currenty_animating = False
		self.destination_x = 0
		self.destination_y = 0
		self.step_size_x = 0
		self.step_size_y = 0
        
	def ShowNotification(self, notification):
		# Set the text of the notification window to reflect the incoming notification message:
		self.notification_text.setText(notification.text)
		# Make sure that the window height does not exceed 2 times the preferred size:
		hinted_size = self.sizeHint()
		if hinted_size.height() < self.preferred_height:
			self.resize(self.maxWidth, self.preferred_height)
		elif hinted_size.height() < 2 * self.preferred_height:
			self.resize(self.maxWidth, hinted_size.height())
		else:
			self.resize(self.maxWidth, 2 * self.preferred_height)
		# Move the new notification window to a suitable place:
		self.MoveImmediately()
		self.show()
		
	def Destroy(self):
		self.displayer.notification_windows.pop(self.handle)
		self.deleteLater()
		self.emit(QtCore.SIGNAL("changeLayout()"))
		
	def CalculateDestination(self):
		dest_x = 0
		dest_y = 0
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
		else:
			last_window_handle = other_handles[-1]
			last_window = self.displayer.notification_windows[last_window_handle]
		
			if self.displayer.direction == "up":
				dest_x = last_window.destination_x
				dest_y = last_window.destination_y - self.height()
			elif self.displayer.direction == "down":
				dest_x = last_window.destination_x
				dest_y = last_window.destination_y + last_window.height()
		
		return (dest_x, dest_y)
		
	def MoveImmediately(self):
		destination = self.CalculateDestination()
		self.move(destination[0], destination[1])
		self.destination_x, self.destination_y = destination
		
	def MoveAnimated(self):
		# Calculate the destination point, animation speed etc:
		destination = self.CalculateDestination()
		self.destination_x, self.destination_y = destination
		
		diff_x = destination[0] - self.x()
		diff_y = destination[1] - self.y()
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
        
class NotificationDisplayer:
    def __init__(self):
        self.tray_icon = NotificationTrayIcon(self,  QtGui.QIcon("icon.png"))
        self.notification_windows = {}
        self.nexthandle = 0
        self.Configure()
    
    def Configure(self):
		# Configurations:
		
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

    def ChangeLayout(self):
    	# Move all currently open notification windows properly:
    	handle_list = self.notification_windows.keys()
    	handle_list.sort()
    	for handle in handle_list:
			self.notification_windows[handle].MoveAnimated()
    
    def DisplayNotification(self, notif):
    	# We dont want any caption or border on our notification displayer window:
		window_flags = QtCore.Qt.WindowFlags() | QtCore.Qt.X11BypassWindowManagerHint
    	# Create a new notification window to display the incoming notification and
    	# append the new notification window to the list of currently open notification windows:
		self.notification_windows[self.nexthandle] = NotificationWindow(displayer = self, handle = self.nexthandle, percent_width = self.percent_width, percent_height = self.percent_height, parent = None, window_flags = window_flags)
		# Attach the changeLayout signal to the corresponding method:
		QtCore.QObject.connect(self.notification_windows[self.nexthandle], QtCore.SIGNAL("changeLayout()"), self.ChangeLayout)		
		# Show the window:
		self.notification_windows[self.nexthandle].ShowNotification(notif)
		self.nexthandle = self.nexthandle + 1
