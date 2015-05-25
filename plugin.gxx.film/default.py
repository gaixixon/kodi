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
xbmcgui.DialogProgress()
 
 
def addCategory(Name, Url, Icon):
                li = xbmcgui.ListItem(Name, iconImage=Icon, thumbnailImage=Icon)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=Url, listitem=li, isFolder=True)
 
def addItem(Name, Url, Icon):
                li = xbmcgui.ListItem(Name, iconImage = Icon)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url = Url, listitem = li)
 
 
 
def list_server():
        print 'nothing'
        addCategory('xemphimhan.com' , base_url+'?action=list_cat&server=xemphimhan.com' , 'DefaultFolder.png')
        #addCategory('xuongphim.tv' , base_url+'?action=list_cat&server=xuongphim.tv' , 'DefaultFolder.png')
        #addCategory('biphim.com' , base_url+'?action=list_cat&server=biphim.com' , 'DefaultFolder.png')
        addCategory('beeg.com' , base_url+'?action=list_ep&server=beeg.com&url=http://beeg.com' , 'DefaultFolder.png')
 
def list_cat():
 if server == 'xemphimhan.com':
        addCategory("Search..", base_url+"?action=list_movie&server="+server, "DefaultFolder.png")
        addCategory("New movie..", base_url+"?action=list_movie&server="+server+"&url=http://m.xemphimhan.com/page-1.html", "DefaultFolder.png")
        content = BeautifulSoup(fetch_web('http://m.xemphimhan.com','mob'))
        for node in content.findAll('li'):
                if '/phim-' in node.a.get('href'):
                        addCategory(node.a.get('title'), base_url+'?action=list_movie&server='+server+'&url=http://m.xemphimhan.com'+node.a.get('href')     ,'DefaultFolder.png')
 elif server =='biphim.com':
        content = BeautifulSoup(urllib2.urlopen('http://biphim.com').read())
        print content
        for node in content.findAll('ul' , {'class' : 'slist'}):
                name = node.li.a.get('title')
                link = node.li.a.get('href')
                logo = 'DefaultFolder.png'
                print name
                addCategory(name, base_url+'?action=list_movie&server=biphim.com&url='+link , logo)            
 
 
 
       
def list_movie():
        global url
        if url == '':
                keyword = search('Nhap ten film can tim:')
                if keyword == False: url = 'http://m.xemphimhan.com/page-1.html'
                else:   url = 'http://m.xemphimhan.com/tim-kiem/'+re.sub("\s+" , "-" , keyword)
                               
        content = BeautifulSoup(fetch_web(url,'mob'))
        for node in content.findAll('div' , {'class' : 'content-items'}):
                link = node.a.get('href')
                name = node.a.get('title')
                logo = node.a.img.get('src')
                addCategory(name, base_url+"?action=list_ep&server="+server+"&url="+link, logo)
        for node in content.findAll('option'):
                link = node.get('value')
                name = node.contents[0]
                logo = 'DefaultFolder.png'
                addCategory(name, base_url+"?action=list_movie&server="+server+"&url="+link, logo)
 
def list_ep():
        global url
        content = BeautifulSoup(fetch_web(url,'mob'))
        if server == 'beeg.com':
         try: logged = args['logged'][0]
         except: logged= 'no'  
         if logged=='yes' or login():
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
                        addItem(name, base_url+"?action=watch&server="+server+"&url="+link, logo)
                       
                        i=i+1
                for node in content.findAll('a'):
                    if '/page-' in node.get('href'):
                        addCategory('Trang: '+str(node.contents[0]) , base_url+'?action=list_ep&server=beeg.com&logged=yes&url=http://beeg.com'+node.get('href')   , 'DefaultFolder.png')
        elif server =='xemphimhan.com':
                for node in content.findAll('a', {'class' : 'btn'}):
                        link = node.get('href')
                        name = 'Tap: '+str(node.contents[0])
                        logo = 'DefaultVideo.png'
                        addItem(name, base_url+"?action=watch&server="+server+"&url="+link, logo)
                       
 
 
 
def watch():
        global url
        content = urllib2.urlopen(url).read()
        if server == 'beeg.com':
                url=re.compile("'720p': '(.+?)'").findall(str(content))
                xbmcgui.DialogProgress().create('', '', 'Loading.. Plz wait!')
                xbmc.Player().play(url[0])
        else:
                url=re.compile('var video_src_mv="(.+?)";').findall(str(content))
                xbmcgui.DialogProgress().create('', '', 'Loading.. Plz wait!')
                xbmc.Player().play(url[0])
 
       
 
try:    action = args['action'][0]
except: action = 'list_server'
try: server = args['server'][0]
except: server=''
try:    cat = args['cat'][0]
except: cat = ''
try:    url = args['url'][0]
except: url = ''
       
if action == 'list_server': list_server()
elif action == 'list_cat': list_cat()
elif action == 'list_movie': list_movie()
elif action == 'list_ep': list_ep()
elif action == 'watch': watch()
 
       
#############  
xbmcplugin.endOfDirectory(addon_handle)
##############
###########