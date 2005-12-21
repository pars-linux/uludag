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
    (Finished,
     RepositoryUpdate,
     NewRepoAdded,
     PisiError,
     PisiInfo,
     PisiNotify,
     AskConfirmation,
     UserConfirmed,
     UpdateProgress,
     UpdateListing,
     PisiAck,
     LastEntry) = range(QEvent.User, QEvent.User+12)

class PisiCommand:
    (AddRepo,
     RemoveRepo,
     UpdateSingleRepo,
     UpdateAllRepos,
     SwapRepos,
     LastEntry) = range(QEvent.User+13, QEvent.User+19)
