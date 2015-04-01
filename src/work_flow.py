import os
import untar
import util
import json
import download_repo
import collect_repos
import check_file_vuls
from datetime import date

data_dir = '../data'
result_dir = '../result'
result_file = 'result.json'
token = os.environ.get('P_TOKEN', None)

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
	#Create result folder and file
	if not os.path.exists(result_dir):
		util.make_folder(result_dir)
	result_file_dir = result_dir + '/' + result_file
	if not os.path.isfile(result_file_dir):
		util.make_file(result_file_dir) 
	#Collect url list
	url_list = collect_repos.collect_repo_urls(token, starting_date)	
	#Write to result file
	with open(result_file_dir) as result_data:
		result_dict = json.load(result_data)
	
	#Create an initial dictionary to collect statistic such as user and repo names
	for url in url_list:
		items = url.split('/')
		username = items[-3]	
		reponame = items[-2]
		if not username in result_dict:
			#result_dict[items[-3]] = [{items[-2]:[]}]
			result_dict[username] = {reponame:[]}
		else:
			#result_dict[items[-3]].append({items[-2]:[]})  
			result_dict[username][reponame] = [] 
		
	#print result_dict	


	print 'Downloading ' + str(len(url_list)) + ' tar files'



	#download_repo.download_url(url_list[0], 0, token)
	#Cautions!!
	#The following code will download less than a thousand repos
	#download_repo.download_urls(url_list, token)
	
	#Uncomment the following line to unleash the beast
	#reponame_to_username = download_repo.download_urls(url_list, token)
	
	dict_dir = result_dir + '/' + 'repo_dict.out'
	############################################################################
	#save repo to user name for testing purpose	
	#with open(dict_dir, 'w') as dwrite:
	#	json.dump(reponame_to_username, dwrite)
	############################################################################
	with open(dict_dir) as d_file:
		reponame_to_username = json.load(d_file)
	
	untar.untar_dir(data_dir)
	util.delete_tarballs(data_dir)
	all_c_files = util.find_extensions('.c', data_dir)
	#print all_c_files

	#Check for files using the vulnerabilities list set up top 
	results = check_file_vuls.scan_files_for_vul(data_dir, all_c_files, vulnerabilities)
	#print results

	#Update the initial result data with vulnerabilities of spefic files in each repo
	for entry in results:
		for key, val in entry.iteritems():
			#print key
			key = key.split('/')
			reponame = key[0]
			last_idx = reponame.rfind('_')
			reponame_no_underscore = reponame[:last_idx]
			filename = key[-1]
			#print reponame_no_underscore + " " + filename
			#print reponame_to_username[reponame]
			username = reponame_to_username[reponame]
			#print result_dict[username]
			result_dict[username][reponame_no_underscore].append({filename: val})
	#print result_dict
	#saving the result
	with open(result_file_dir, 'w') as outfile:	
		json.dump(result_dict, outfile) 
