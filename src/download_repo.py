from subprocess import call, Popen, PIPE

def download_url(url, file_num): 
	file_name = '../data/' + url.split('/')[-2] + '_' + str(file_num)  + '.tar.gz'
	print 'Downloading from ' + url + ' save as ' + file_name.split('/')[-1]
	cmd = 'curl -L ' + url 
	#print cmd
	args = cmd.split()
	f = open(file_name,'w')
	subp = Popen(args, stdout=f, stderr=PIPE)

	curlstdout, curlstderr = subp.communicate()
	#print curlstderr
	
def download_urls(url_list):
	file_num = 1
	for url in url_list:
		print 'File ' + str(file_num)
		download_url(url, file_num)
		file_num += 1

def make_folder(folder_name):
	print 'Creating folder ' + folder_name + '...'
	call(["mkdir", folder_name])
	
#call(["ls", "-l"])
#call(["curl", "-L", url])
