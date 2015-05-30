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
from WebScraper import *

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
 
xbmcplugin.setContent(addon_handle, 'movies')
 
def list_server():
        addItem('xemphimhan.com' , base_url+'?action=list_cat&server=xemphimhan.com' , 'DefaultFolder.png', 1)
        addItem('xuongphim.tv' , base_url+'?action=list_cat&server=xuongphim.tv' , 'DefaultFolder.png', 1)
        #addItem('youtest' , 'plugin://plugin.video.youtube/play/?video_id=an1WlTDoOaA' , 'DefaultFolder.png',0)
	   #addItem('biphim.com' , base_url+'?action=list_cat&server=biphim.com' , 'DefaultFolder.png',1)
 
        
       
def list_movie():
 global url
 if server == 'xemphimhan.com':
        if url == '':
                keyword = search('Nhap ten film can tim:')
                if keyword == False: url = 'http://m.xemphimhan.com/page-1.html'
                else:   url = 'http://m.xemphimhan.com/tim-kiem/'+re.sub("\s+" , "-" , keyword)
                               
        content = BeautifulSoup(fetch_web(url,'mob'))
        for node in content.findAll('div' , {'class' : 'content-items'}):
                link = node.a.get('href')
                name = node.a.get('title')
                logo = node.a.img.get('src')
                addItem(name, base_url+"?action=list_ep&server="+server+"&url="+link, logo, 1)
        for node in content.findAll('option'):
                link = node.get('value')
                name = node.contents[0]
                logo = 'DefaultFolder.png'
                addItem(name, base_url+"?action=list_movie&server="+server+"&url="+link, logo, 1)
 if server == 'xuongphim.tv':
	if url == '':
		keyword=search('Nhap ten film can tim:')
		if keyword == False: url = 'http://xuongphim.tv/tim-kiem/-/trang-1.html'
		else: url = 'http://xuongphim.tv/tim-kiem/'+re.sub('\s+', '-', keyword)+'.html'
		content = BeautifulSoup(fetch_web(url,'web'))
		for node in content.findAll('div' , {'class' : 'tn-bxitem'}):
			link = 'http://xuongphim.tv'+node.a.get('href')
			logo = node.a.span.img.get('src')
			name = node.a.span.img.get('alt')
			addItem(name, base_url+"?action=list_ep&server="+server+"&url="+link, logo, 1)
		########pagination not worked yet.. because the stupidity of inconsistency in search and web & mobile view style
		'''for node in content.findAll('a' , {'rel' : 'nofollow'}):
			link = 'http://xuongphim.tv'+node.get('href')
			logo = 'DefaultVideo.png'
			name = 'Trang: '+str(node.string)
			addItem(name, base_url+"?action=list_movie&server="+server+"&url="+link, logo, 1)'''
		
	else:
		content = BeautifulSoup(fetch_web(url,'mob'))
		for node in content.findAll('div' , {'class' : 'content-items'}):
			link = node.a.get('href')
			name = node.a.get('title')
			logo = node.a.img.get('src')
			addItem(name, base_url+"?action=list_ep&server="+server+"&url=http://xuongphim.tv"+link, logo, 1)
		for node in content.findAll('option'):
			link = 'http://xuongphim.tv'+node.get('value')
			name = node.string
			logo = 'DefaultVideo.png'
			addItem(name, base_url+"?action=list_movie&server="+server+"&url="+link, logo, 1)

def list_ep():
	content = BeautifulSoup(fetch_web(url,'mob'))
	if server =='xemphimhan.com':
                for node in content.findAll('a', {'class' : 'btn'}):
                        link = node.get('href')
                        name = 'Tap: '+str(node.contents[0])
                        logo = 'DefaultVideo.png'
                        addItem(name, base_url+"?action=watch&server="+server+"&url="+link, logo, 0)
                       
	elif server =='xuongphim.tv':
		for node in content.findAll('a' , {'class' : 'btn'}):
			name = 'Tap: '+node.string
			link = 'http://xuongphim.tv'+node.get('href')
			logo = 'DefaultVideo.png'
			addItem(name, base_url+'?action=watch&server='+server+'&url='+link, logo, 0)
 
 
try:    action = args['action'][0]
except: action = 'list_server'
try: server = args['server'][0]
except: server=''
try:    cat = args['cat'][0]
except: cat = ''
try:    url = args['url'][0]
except: url = ''
       
if action == 'list_server': list_server()
elif action == 'list_cat': list_cat(server)
elif action == 'list_movie': list_movie()
elif action == 'list_ep': list_ep()
elif action == 'watch': watch(server, url)
 
       
#############  
xbmcplugin.endOfDirectory(addon_handle)
##############
###########