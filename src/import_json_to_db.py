import os
import save_data as sd
from imp import reload
reload(sd)

def import_to_database (json_dict, credentials_file):
#	number_of_files = 0	
	db_conn = sd.get_connection(credentials_file);
	for username, repo in json_dict.iteritems():
		sd.save_user_data(db_conn, username);
		#print username
		for reponame, repo_dict in repo.iteritems():
			date_created = repo_dict["created_at"]
			repo_size = repo_dict["size"]
			last_pushed = repo_dict["pushed_at"]
			contributors_url = repo_dict["contributors_url"]
			#print date_created
			#print repo_size
			#print last_pushed
			repo_id = sd.save_repo_data(db_conn, reponame, date_created, username, repo_size, last_pushed, contributors_url);
			file_list = repo_dict["files"];
			#print file_list
			for file_info in file_list:
				#print file_info
				for filename, vuls in file_info.iteritems():
# TODO: add file hash?
					file_id = sd.save_file_data(db_conn, filename, repo_id, ""); 
					#print filename
				 	for vul_info in vuls:
						#print vul_info
						for vul, places in vul_info.iteritems():
							#print vul
							for p in places:
								#print k
								sd.save_vulnerability_data(db_conn, file_id, -1, p, vul);
#							if vul == func:
#								number_of_files += 1
#	return number_of_files

def collect_num_files_using_func_list(json_dict, func_list):
	num_file_list = []
	for func in func_list:
		num_file_list.append(collect_num_files_using_func(json_dict, func))
	return num_file_list
							
			
