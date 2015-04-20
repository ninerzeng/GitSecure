import os
import save_data as sd
from imp import reload
reload(sd)

def import_to_database (json_dict, credentials_file):
#	number_of_files = 0	
	db_conn = sd.get_connection(credentials_file);
#	start = json_dict["start"]
#	end = json_dict["end"]
#	json_dict = json_dict["result"]
	for username, repo in json_dict.iteritems():
		sd.save_user_data(db_conn, username);
		#print username
		for reponame, repo_dict in repo.iteritems():
			date_created = repo_dict["created_at"]
			repo_size = repo_dict["size"]
			last_pushed = repo_dict["pushed_at"]
			contributors_url = repo_dict["contributors_url"]
			description = repo_dict["description"]
			repo_id = sd.save_repo_data(db_conn, reponame, date_created, username, repo_size, last_pushed, repo_dict["url"], repo_dict["forks_url"], contributors_url, description, repo_dict["stargazers"], repo_dict["forks"]);

			file_list = repo_dict["files"];
			for file_entry in file_list:
				#print file_info
				for filename, datapoints in file_entry.iteritems():
					file_id = sd.save_file_data(db_conn, filename, repo_id, "") 
				 	for thing in datapoints:
						line = thing["line"]
						code_sample = thing["code_sample"]
						sd.save_vulnerability_data(db_conn, file_id, line, code_sample);

def collect_num_files_using_func_list(json_dict, func_list):
	num_file_list = []
	for func in func_list:
		num_file_list.append(collect_num_files_using_func(json_dict, func))
	return num_file_list
							
			
