#!/usr/bin/env python
# -*- coding: utf-8 -*-

SITENAME = "Uludağ Haftalık Bülteni"
LOGS = "bultenler"
ARCHIVE = "arsiv"

entry_count = 0 # entries printed in first page

index_file = LOGS + "/.index"
log_prefix = ".txt"

header_text = '''<!--#include file="header.html" -->
<div class="sayfa">
'''

footer_text = '''
</div>
<!--#include file="footer.html" -->
'''
