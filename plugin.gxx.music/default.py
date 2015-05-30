#!/usr/bin/python
# coding=utf-8

import urlparse
import xbmcplugin
from BeautifulSoup import BeautifulSoup
#from MyClass import *

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'music')

addItem


#########
xbmcplugin.endOfDirectory(addon_handle)
##########
#########