import os
def collect_num_files_using_func (json_dict, func):
	number_of_files = 0	
	for username, repo in json_dict.iteritems():
		#print username
		for reponame, file_list in repo.iteritems():
			#print file_list
			for file_info in file_list:
				#print file_info
				for filename, vuls in file_info.iteritems():
					#print filename
				 	for vul_info in vuls:
						#print vul_info
						for vul, places in vul_info.iteritems():
							#print vul
							if vul == func:
								number_of_files += 1
	return number_of_files

def collect_num_files_using_func_list(json_dict, func_list):
	num_file_list = []
	for func in func_list:
		num_file_list.append(collect_num_files_using_func(json_dict, func))
	return num_file_list
							
			
