import xml.etree.cElementTree as ET
import subprocess
import json

# unique path 
# [name of file]:
#	{[Type]:
#		[line number 1]
#		[line number 2]
#	[Type2]
#		[line number 1]
#		[line number 2]
#	}


def parse(result_SA_file_dir, reponame_to_username, result_dict ):
	with open("../result/rats.xml", 'w') as outfile:
		subprocess.check_call(["rats", "--xml", "../data" ], stdout=outfile)

	tree = ET.ElementTree(file='../result/rats.xml')
	for elem in tree.iter(tag = 'total_time'):
		print "Time spent by static analyzer: " + elem.text
	for elem in tree.iter(tag = 'vulnerability'):
		vulnerability = ""
		i = 0
		# first we check if there is a  <type>
		for e in  elem.iterfind('type'):	
			vulnerability = e.text
			i = 1
		# print vulnerability
		# if we have no types then we move on to next vulernability tree
		if i == 0:
			continue
		for f in elem.iterfind('file'):
			# here we parse the file name
			key = f[0].text # this accesses <name> tag
			# structure is [reponame]/[path to file]
			# first find the path to file

			key = key[8:]

			first_idx = key.find('/')
			unique_path = key[first_idx+1:]
			# second grab the repo name
			# and remove the extra numbers
			# at the end
			key = key.split('/')
			reponame = key[0]
			last_idx = reponame.rfind('_')
			reponame_no_underscore = reponame[:last_idx]
			# then we grab the name of the file after splitting key var
			filename = key[-1]
			#print reponame_no_underscore + " " + filename
			#print reponame_to_username[reponame]
			# then we look up the username in our dictionary

			username = reponame_to_username[reponame]
			# print username

			#print result_dict[username]
			line_number = []
			for l in f.iterfind('line'):
				line_number.append(l.text)

			# here we construct val
			val = []
			val.append ({ vulnerability : line_number })

			# we only want to add the file : [ vulnerability dict ] if 
			# we havent already encountered this file

			unique = 1
			# print vulnerability, val, line_number, reponame_no_underscore, unique_path

			# if the file exists as a dictionary row then we append to that file
			for dictionary_for_file in result_dict[username][reponame_no_underscore]['files']:
				if unique_path in dictionary_for_file.keys():
					# print "not unique"
					unique = 0
					dictionary_for_file[unique_path].append( { vulnerability : line_number})
					break
			if unique == 1:
				result_dict[username][reponame_no_underscore]['files'].append({unique_path: val})

	with open(result_SA_file_dir,'w') as outfile:	
		json.dump(result_dict, outfile, ensure_ascii=False) 
	return result_dict

