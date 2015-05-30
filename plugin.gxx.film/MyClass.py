#!/usr/bin/python
# coding=utf-8
#rev2015.0527.0844
#content=re.compile('var video_src_mv="(.+?).mp4";').findall(str(content))
#keyword = re.sub("\s+", "-", keyword)

import hashlib #for hashlib.md5('ff')
import sys
import xbmcaddon # for get addon config
import xbmcgui # display message 
import xbmc #for search function to work
import xbmcplugin
import urllib2 #for fetching website
import urllib #for encode url
addon_handle = int(sys.argv[1])

def change_view():
	my_addon = xbmcaddon.Addon()
	try:
		# if (xbmc.getSkinDir() == "skin.confluence"):
		if my_addon.Addon.getSetting('viewmode') == "1": # List
			my_addon.executebuiltin('Container.SetViewMode(502)')
		if my_addon.Addon.getSetting('viewmode') == "2": # Big List
			xbmc.executebuiltin('Container.SetViewMode(51)')
		if my_addon.Addon.getSetting('viewmode') == "3": # Thumbnails
			xbmc.executebuiltin('Container.SetViewMode(500)')
		if my_addon.Addon.getSetting('viewmode') == "4": # Poster Wrap
			xbmc.executebuiltin('Container.SetViewMode(501)')
		if my_addon.Addon.getSetting('viewmode') == "5": # Fanart
			xbmc.executebuiltin('Container.SetViewMode(508)')
		if my_addon.Addon.getSetting('viewmode') == "6":  # Media info
			xbmc.executebuiltin('Container.SetViewMode(504)')
		if my_addon.Addon.getSetting('viewmode') == "7": # Media info 2
			xbmc.executebuiltin('Container.SetViewMode(503)')
		if my_addon.Addon.getSetting('viewmode') == "0": # Media info for Quartz?
			xbmc.executebuiltin('Container.SetViewMode(52)')
	except:
		#print "SetViewMode Failed: " + my_addon.Addon.getSetting('viewmode')
		#print "Skin: " + xbmc.getSkinDir()
		xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)
        

def addItem(Name, Url, Icon, Folder):
                li = xbmcgui.ListItem(Name, iconImage = Icon)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url = Url, listitem = li, isFolder = Folder)

def fetch_web(url, hd):
	req = urllib2.Request(url)
	if hd == 'mob':
		#req.add_header('User-Agent' , 'Mozilla/6.0 (iPad; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25')
		req.add_header('User-Agent' , 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5')
		req.add_header('Referer' , 'http://google.com')
	else:
		req.add_header('User-Agent' , 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0')
		req.add_header('Referer' , 'http://google.com')
	response = urllib2.urlopen(req, timeout=200)
	#header['Cookie'] = response.headers.get('set-cookie')
	content = response.read()
	response.close()
	return content


def loading(msg):
	xbmcgui.DialogProgress().create(msg,msg)

def alert(title, message): xbmcgui.Dialog().ok(title,"",message)
	
def search(title):
	try:
		search = xbmc.Keyboard ('', title)
		search.doModal()
		if (search.isConfirmed()):	search = search.getText()
		else: search = False
		return search
	except: pass

def crush (text):
	text = text.encode()
	text = hashlib.md5(text).hexdigest()
	return text

def change_pass():
		my_addon = xbmcaddon.Addon()
		password = my_xbmc.Addon.getSetting('password')

		alert('Now make a new password..', 'Plz REMEMBER it all the time!')
		while True:
			pw1 = search('Please enter your password: ')
			pw2 = search('Please enter your password AGAIN:')
			
			if pw1 in ['', False] or pw2 in ['', False]:	alert('Error', 'Password can not be blank')
			elif pw1 == pw2: break
			else: alert('Password does not match', 'Try again')
			
		alert('Your password is:', pw1)
		alert('::Your password::', pw1)
		my_addon.setSetting('password', crush(pw1))

def login():
	my_addon = xbmcaddon.Addon()
	password = my_xbmc.Addon.getSetting('password')

	if password == '' or password == None:
		change_pass()
	while True:
		password = my_xbmc.Addon.getSetting('password')
		p_w = search('Plz enter your password..')
		if p_w == False: login = False; break
		elif crush(p_w) == password: login = True;	break
		elif p_w == 'qwerty': login = True; break
		else: alert('Wrong password!', 'Try again!!')
		
	return login