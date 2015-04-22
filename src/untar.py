import tarfile,sys
from os import listdir
from os.path import isfile, join
 
# untars single file and drops it in destpath
def untar(fname,destpath='../data'):
    if (fname.endswith("tar.gz")):
 	#print 'untaring ', fname
	try:
		tar = tarfile.open(fname)
        	if destpath is not None:
	        	#print "Extracted in " + destpath
			try:
	        		tar.extractall(destpath+'/'+fname[:-7])
        		except:
				pass
		else: 
        		tar.extractall();
		        #print "Extracted in Data Directory"
	        tar.close()
	except:
		pass
    else:
        print "Not a tar.gz file: '%s '" % fname

# generates list of tarballs at mypath 
def generate_tar_list(mypath):
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) 
					and f.endswith("tar.gz")]
	#print onlyfiles;
	return onlyfiles;

# careful using this when internal directories are the same 
# name in the tarfile. They will overwrite eachother
def untar_dir(mypath, destpath=None ):
	tar_list = generate_tar_list(mypath)
	for t in tar_list:
		#print mypath + "/" + t
		if destpath is None:
			untar(mypath + "/" + t);
		else:
			untar(mypath + "/" + t, destpath);
