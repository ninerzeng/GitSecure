import os
import untar
import util
import json
import download_repo
import collect_repos
import check_file_vuls
from datetime import date
import datetime
import save_data as sd

data_dir = '../data'
#result_dir = '../result'
#result_file = 'result.json'
token = os.environ.get('P_TOKEN', None)
mysqlcred_file = "mysqlcreds-remote.csv"

#List of vulnerable functions to check
vulnerabilities = ['gets', 'getpw', 'printf', 'fprintf', 'sprintf', 'snprintf', 'vsprintf', 'strcpy', 'strcat', 'scanf', 'rand', 'vfork']
#Get folders prior to Jan 1st, 2009
starting_date = date(2009,1,1)
if __name__ == '__main__':
	#Token to raise GitHub rate limit constraint
	if not token:
		print 'Forgot to export your token'
	#Create folder data if it does not exist already
	if not os.path.exists(data_dir):
		util.make_folder(data_dir)
	#Collect url list
	url_list = collect_repos.collect_repo_urls(token, starting_date)	
	
	#Create an initial dictionary to collect statistic such as user and repo names
	db_conn = sd.get_connection(mysqlcred_file);
	file_num = 1
	for item in url_list:
		url = item['url']
		repo_size = item['size']
		repo_created_at = item['created_at']
		items = url.split('/')
		username = items[-3]	
		reponame = items[-2]
		#TODO: insert user into database, hold onto username
		sd.save_user_data(db_conn, username);
		#print "user: " + username
		#TODO: insert repo into database, save repo_id
		repo_id = sd.save_repo_data(db_conn, reponame, repo_created_at , username, repo_size, datetime.datetime.now());
		#print "repo: " + reponame
		download_repo.download_url(url, file_num, token)
		print "Downloaded repo ", file_num
		file_num+=1;
		#TODO: these steps are all going to be extra slow because they're designed to compute in batch and that's now what we're doing
		untar.untar_dir(data_dir)
		util.delete_tarballs(data_dir)
		all_c_files = util.find_extensions('.c', data_dir)
		for c_file in all_c_files:
			filename = c_file[c_file.find('/'):]
			#print "file: " + filename
			#TODO: insert file into db, save file_id
			file_id = sd.save_file_data(db_conn, filename, repo_id, '')
			results = check_file_vuls.scan_files_for_vul(data_dir, {c_file}, vulnerabilities);
			for entry in results:
				for key, val in entry.iteritems():
					#print "key ", key
					#print "val ", val
					for vuln_set in val:
						for func, ar in vuln_set.iteritems():
							for sentence in ar:
								#print func, " ", sentence
								sd.save_vulnerability_data(db_conn, file_id, -1, sentence, func)





