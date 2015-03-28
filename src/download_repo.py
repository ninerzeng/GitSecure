from subprocess import call
import pycurl
import StringIO
import json

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
	header = StringIO.StringIO()
	f = open(file_name,'w')
	c = pycurl.Curl()
	c.setopt(pycurl.URL,url)
	c.setopt(pycurl.WRITEDATA, f)
	c.setopt(c.FOLLOWLOCATION, True)
	c.setopt(c.HEADERFUNCTION, header.write)
	#Authorizaiton token
	if token:
		c.setopt(pycurl.HTTPHEADER, ['Authorization: token ' + str(token)])
	c.setopt(pycurl.SSL_VERIFYPEER, True)
	c.setopt(pycurl.SSL_VERIFYHOST, 2)
	c.perform()
	f.close()
	print ('Status: %d' % c.getinfo(c.RESPONSE_CODE))
	#print header.getvalue()
	c.close()

def download_urls(url_list, token=None):
	file_num = 1
	for url in url_list:
		print 'File ' + str(file_num)
		download_url(url, file_num, token)
		file_num += 1
	
def make_folder(folder_name):
	print 'Creating folder ' + folder_name + '...'
	call(["mkdir", folder_name])
	
#call(["ls", "-l"])
#call(["curl", "-L", url])
