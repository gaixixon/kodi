#!/usr/bin/python
# coding=utf-8
#rev2015.0528.0857
from MyClass import *
import re
import xbmc
from BeautifulSoup import BeautifulSoup
base_url = sys.argv[0]


##############list cat
def list_cat(server):
 if server == 'xemphimhan.com':
        addItem("Search..", base_url+"?action=list_movie&server="+server, "DefaultFolder.png",1)
        addItem("New movie..", base_url+"?action=list_movie&server="+server+"&url=http://m.xemphimhan.com/page-1.html", "DefaultFolder.png",1)
        content = BeautifulSoup(fetch_web('http://m.xemphimhan.com','mob'))
        for node in content.findAll('li'):
                if '/phim-' in node.a.get('href'):
                        addItem(node.a.get('title'), base_url+'?action=list_movie&server='+server+'&url=http://m.xemphimhan.com'+node.a.get('href')     ,'DefaultFolder.png', 1)
 elif server == 'xuongphim.tv':
	addItem('Search..' , base_url+'?action=list_movie&server='+server, 'DefaultVideo.png', 1)
        content = BeautifulSoup(fetch_web('http://xuongphim.tv', 'mob'))
        for node in content.findAll('li'):
                name = node.a.string
		link = node.a.get('href')
                logo = 'DefaultFolder.png'
                if link.startswith('/'): addItem(name, base_url+'?action=list_movie&server=xuongphim.tv&url=http://xuongphim.tv'+link , logo, 1)            

##############list cat
 
#####################watch
def watch(server, url):
	content = fetch_web(url, 'mob')
	#content = urllib2.urlopen(url).read()
	
	if server == 'xemphimhan.com':
		url=re.compile('var video_src_mv="(.+?)";').findall(str(content))

	elif server == 'xuongphim.tv':
		url = re.compile('file: "(.+?)"').findall(str(content))
		print content
		print url
		if url == []:
			url = re.compile('sources: \[(.*),\],').findall(str(content))
			if 'tv.zing.vn' in url[0]: url = get_zing(url[0])
	loading('Please wait..')       
	try: xbmc.Player().play(url[1])
	except: xbmc.Player().play(url[0])

def get_zing(url):
	content = fetch_web(url, 'mob')
	url = re.compile('<source src="(.+?)"').findall(str(content))
	print content
	print url
	return url
#####################watch 
