# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors:  İsmail Dönmez <ismail@uludag.org.tr>

from qt import QEvent

class CustomEvent:
	Finished = QEvent.User+1
	RepositoryUpdate = QEvent.User+2
	PisiError = QEvent.User+3
	PisiInfo = QEvent.User+4
	PisiNotify = QEvent.User+5
	AskConfirmation = QEvent.User+6
	UserConfirmed = QEvent.User+7
	UpdateProgress = QEvent.User+8
	UpdateListing = QEvent.User+9
