#!/usr/bin/python
# coding=utf-8

import urllib2
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import re
from BeautifulSoup import BeautifulSoup

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'movies')

try: channel = args['channel'][0]
except: channel = None

def addCategory(Name, Url, Icon):
		li = xbmcgui.ListItem(Name, iconImage=Icon)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=Url, listitem=li, isFolder=True)

def addItem(Name, Url, Icon):
		li = xbmcgui.ListItem(Name, iconImage = Icon)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url = Url, listitem = li)

def soup(url):
	url = urllib2.urlopen(url)
	soup = BeautifulSoup(url.read())
	return soup


if channel == None:
		url= 'http://hplus.com.vn/vi/categories/live-tv/'
		soup = soup(url)
		for node in soup.findAll('a', {'class' : 'tooltips'}):
			tvlink = 'http://hplus.com.vn/'+node.get('href') 
			tvname = node.h3.string          
			tvlogo = node.get('style')[23:-2] 
			addItem(tvname, base_url+"?channel="+tvlink, tvlogo)
	
else:
		req = urllib2.Request(channel)
		#req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0')
		response=urllib2.urlopen(req)
		#cooki = response.headers.get('set-cookie')
		content=response.read()
		tvlink=re.compile('var iosUrl = "(.+?)";').findall(str(content))
		foo = urllib2.urlopen(tvlink[0]).read()
		xbmc.Player().play(tvlink[0])
		
xbmcplugin.endOfDirectory(addon_handle)