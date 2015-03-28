from subprocess import call
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
