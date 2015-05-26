#!/usr/bin/python
# coding=utf8
 
import sys
import urllib
import urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
 
import re
from BeautifulSoup import BeautifulSoup
from MyClass import *
 
base_url = sys.argv[0]
addon_handle = int(sys.argv[1]) #THIS MUST BE ON TOP
args = urlparse.parse_qs(sys.argv[2][1:])
 
xbmcplugin.setContent(addon_handle, 'movies')
 
 
def addItem(Name, Url, Icon, Folder):
                li = xbmcgui.ListItem(Name, iconImage = Icon)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url = Url, listitem = li, isFolder = Folder)
 
def list_ep():
  	if logged=='yes' or login():
		addItem('[COLOR red]>>Change password<<[/COLOR]', base_url+'?action=change_pass' , 'DefaultFolder.png', 0)
	        content = BeautifulSoup(fetch_web(url,'mob'))
                node = re.compile('var tumbalt =(.*);').findall(str(content))
                node = str(node)[4:-4]
                node = re.sub("','" , "_", node)               
                node = node.split('_')
 
                nod = re.compile('var tumbid(.*);').findall(str(content))
                nod =str(nod)[6:-3]    
                nod =nod.split(',')
                i=0
                for node in node:
                        link = 'http://beeg.com/'+str(nod[i])
                        name = node
                        logo = 'http://img.beeg.com/236x177/'+str(nod[i])+'.jpg'
                        addItem(name, base_url+"?action=watch&url="+link, logo, 0)
                       
                        i=i+1
                for node in content.findAll('a'):
                    if '/page-' in node.get('href'):
                        addItem('Trang: '+str(node.contents[0]) , base_url+'?action=list_ep&logged=yes&url=http://beeg.com'+node.get('href')   , 'DefaultFolder.png', 1)
 
def watch():
        global url
        content = urllib2.urlopen(url).read()
        url=re.compile("'720p': '(.+?)'").findall(str(content))
        xbmcgui.DialogProgress().create('', '', 'Loading.. Plz wait!')
        xbmc.Player().play(url[0])
 
try:    action = args['action'][0]
except: action = 'list_ep'
try:    url = args['url'][0]
except: url = 'http://beeg.com'
try: logged = args['logged'][0]
except: logged= 'no'  
       

if action == 'list_ep': list_ep()
elif action == 'change_pass': change_pass()
else: watch()
       
#############  
xbmcplugin.endOfDirectory(addon_handle)
##############
###########