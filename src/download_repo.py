from subprocess import call, Popen, PIPE

def download_url(url): 
	print url
	call(["ls", "-l"])
	#call(["curl", "-L", url])
	file_name = '../data/' + url.split('/')[-2] + '.tar.gz'
	print file_name
	cmd = 'curl -L ' + url 
	print cmd
	args = cmd.split()
	f = open(file_name,'w')
	subp = Popen(args, stdout=f, stderr=PIPE)

	curlstdout, curlstderr = subp.communicate()
	#print curlstderr
	
def download_urls(url_list):
	for url in url_list:
		download_url(url)
def make_folder(folder_name):
	call(["mkdir", folder_name])
	
