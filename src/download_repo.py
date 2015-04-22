from subprocess import call
import pycurl
import StringIO
import json
import util
import os

def download_url(url, file_num='', token=None): 
	file_name = '../data/' + url.split('/')[-2] + '_' + str(file_num)  + '.tar.gz'
	print 'Downloading from ' + url + ' save as ' + file_name.split('/')[-1]
	'''	
	cmd = 'curl -L ' + url 
	#print cmd
	args = cmd.split()
	f = open(file_name,'w')
	subp = Popen(args, stdout=f, stderr=PIPE)
	curlstdout, curlstderr = subp.communicate()
	f.close()
	#print curlstderr
	
	'''
	headers = {}
	def header_function(header_line):
	    # HTTP standard specifies that headers are encoded in iso-8859-1.
	    # On Python 2, decoding step can be skipped.
	    # On Python 3, decoding step is required.
	    header_line = header_line.decode('iso-8859-1')

	    # Header lines include the first status line (HTTP/1.x ...).
	    # We are going to ignore all lines that don't have a colon in them.
	    # This will botch headers that are split on multiple lines...
	    if ':' not in header_line:
		return

	    # Break the header line into header name and value.
	    name, value = header_line.split(':', 1)

	    # Remove whitespace that may be present.
	    # Header lines include the trailing newline, and there may be whitespace
	    # around the colon.
	    name = name.strip()
	    value = value.strip()

	    # Header names are case insensitive.
	    # Lowercase name here.
	    name = name.lower()

	    # Now we can actually record the header name and value.
	    headers[name] = value

	#header = StringIO.StringIO()
	f = open(file_name,'w')
	c = pycurl.Curl()
	c.setopt(pycurl.URL, str(url))
	c.setopt(pycurl.WRITEDATA, f)
	c.setopt(c.FOLLOWLOCATION, True)
	c.setopt(c.HEADERFUNCTION, header_function)
	#Authorizaiton token
	if token:
		c.setopt(pycurl.HTTPHEADER, ['Authorization: token ' + str(token)])
	c.setopt(pycurl.SSL_VERIFYPEER, True)
	c.setopt(pycurl.SSL_VERIFYHOST, 2)
	c.perform()
	f.close()
	status = int(c.getinfo(c.RESPONSE_CODE))	
	if status != 200:
		print ('Status: %d' % status)
		os.remove(file_name)
	#print header.getvalue()
	#print headers
	c.close()
	ratelimit_remaining = int(headers['x-ratelimit-remaining'])
	reset_time = int(headers['x-ratelimit-reset'])
	#print ratelimit_remaining
	#print reset_time
	if ratelimit_remaining == 0: 
		util.nap(reset_time)

def download_urls(url_list, token=None):
	repo_to_user = {}
	file_num = 1	
	for url in url_list:
		#print 'File ' + str(file_num)
		download_url(url, file_num, token)
		repo_to_user[url.split('/')[-2] + '_' + str(file_num)] = url.split('/')[-3]
		file_num += 1
	return repo_to_user
	
def make_folder(folder_name):
	print 'Creating folder ' + folder_name + '...'
	call(["mkdir", folder_name])
	