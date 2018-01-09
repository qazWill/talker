import urllib2

def getgoogleurl(search,siteurl=False):
	if siteurl==False:
		return 'http://www.google.com/search?q='+urllib2.quote(search)
	else:
		return 'http://www.google.com/search?q=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)

def getgooglelinks(search,siteurl=False):
	headers = {'User-agent':'Mozilla/11.0'}
	req = urllib2.Request(getgoogleurl(search,siteurl),None,headers)
	site = urllib2.urlopen(req)
	data = site.read()
	site.close()
	start = 0
	while start < len(data):
		start = data.find('href=', start)
		if start == -1:
			break
		end = data.find('"', start + 1)
		end = data.find('"', end + 1)
		print data[start:end]
		start = end + 1
		print start


links = getgooglelinks('python')
