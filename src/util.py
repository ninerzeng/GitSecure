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

def find_extensions(ext, path = None):
	print "Listing files with extension " + ext
	victim = ""
	if path is not None:
		victim = path + "/*." + ext
	matches = []
	for root, dirnames, filenames in os.walk(path):
		for filename in filenames:
			'''
			print root
			print filename
			print dirnames
			'''
			if filename.endswith(ext):
				path_file = os.path.join(root, filename)
				matches.append(path_file[len(path)+1:])
	return matches

def delete_in_directory(folder):
	# folder = '/path/to/folder'
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path): 
				shutil.rmtree(file_path)
		except Exception, e:
			print e
