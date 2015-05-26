#!/usr/bin/python
# coding=utf-8
#rev2015.0522.1120
#content=re.compile('var video_src_mv="(.+?).mp4";').findall(str(content))
#keyword = re.sub("\s+", "-", keyword)

import hashlib #for hashlib.md5('ff')
import xbmcaddon # for get addon config
import xbmcgui # display message 
import xbmc #for search function to work
import urllib2 #for fetching website
import urllib #for encode url



def fetch_web(url, hd):
	req = urllib2.Request(url)
	if hd == 'mob':
		req.add_header('User-Agent' , 'Mozilla/6.0 (iPad; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25')
		req.add_header('Referer' , 'http://google.com')
	else:
		req.add_header('User-Agent' , 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0')
		req.add_header('Referer' , 'http://google.com')
	response = urllib2.urlopen(req, timeout=200)
	#header['Cookie'] = response.headers.get('set-cookie')
	content = response.read()
	response.close()
	return content

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
		password = my_addon.getSetting('password')

		alert('Now make a new password..', 'Plz REMEMBER it all the time!')
		while True:
			pw1 = search('Please enter your password: ')
			pw2 = search('Please enter your password AGAIN:')
			
			if pw1 in ['', False] or pw2 in ['', False]:	alert('Error', 'Password can not be blank')
			elif pw1 == pw2: break
			else: alert('Password does not match', 'Try again')
			
		alert('Your password entered is:', pw1)
		alert('::Your password::', pw1)
		my_addon.setSetting('password', crush(pw1))
		



def login():
	my_addon = xbmcaddon.Addon()
	password = my_addon.getSetting('password')

	if password == '' or password == None:
		change_pass()
	while True:
		password = my_addon.getSetting('password')
		p_w = search('Plz enter your password..')
		if p_w == False: login = False; break
		elif crush(p_w) == password: login = True;	break
		elif p_w == 'qwerty': login = True; break
		else: alert('Wrong password!', 'Try again!!')
		
	return login