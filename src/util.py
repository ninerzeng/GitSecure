import os
from subprocess import call
from glob import glob
def make_folder(folder_name):
	print 'Creating folder ' + folder_name + '...'
	call(["mkdir", folder_name])

def make_file(file_name):
	print 'Creating file ' + file_name + '...'
	call(["touch", file_name])
	#echo_line = 'echo "\\\"result_dict\\\": {}" >> ' + file_name
	echo_line = 'echo "{}" >> ' + file_name
	print echo_line
	call(echo_line, shell=True)  

def delete_files_with_extension(ext, path=None):
	print "Deleteing files with extension " + ext
	victim = ""
	if path is not None:
		victim = path + "/*." + ext
	else:
		victim = "*." + ext
	for v in glob(victim):
		os.remove(v)
# deletes all tars in the path directory
# if no path is provided delete ones in current dir
def delete_tarballs(dirpath=None):	
	delete_files_with_extension("tar.gz", dirpath)

