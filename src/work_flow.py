import os
import untar
import util
import json
import download_repo
import collect_repos
import check_file_vuls
import analyze_json
from datetime import date, timedelta
import math
import time
import import_json_to_db
import static_analysis_module as SA
data_dir = '../data'
result_dir = '../result'
result_file = 'result.json'
token = os.environ.get('Ninas_P_TOKEN', None)
credentials_file='mysqlcreds-remote.csv'

#List of vulnerable functions to check
vulnerabilities = ['strcpy', 'strcat', 'sprintf', 'vsprintf', 'gets', 'getpw']
#Corresponding good practices
good_practices = ['strncpy', 'strncat', 'snprintf', 'vsnprintf', 'fgets', 'getpwuid', 'strlcpy', 'strlcat']

#Get folders prior to Jan 1st, 2009
#starting_date = date(2009,1,1)
starting_date = date(2014,1,1)
ending_date = date(2014,1,2)
#ending_date = date.today()
#ending_date = date(2008,3,5)
initial_delta = timedelta(days=1 )
#initial_delta = timedelta(days=5)

#Stats
total_num_of_repo_queried = 0
total_num_of_repo_downloaded = 0
total_seconds_of_download = 0
total_seconds_of_analyzing = 0


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
	ps = None
	pe = None
	#Use this set to download prior as well
	#cs = None
	#ce = starting_date
	#User this set to download inclusive
	cs = starting_date
	ce = cs + initial_delta
	print 'Starting date is ', starting_date, ' and ending date is ', ending_date

	while (not pe or pe < ending_date):		
		if not cs:
			meta_list_with_count = collect_repos.collect_repo_urls(token, ce)	
		else:
			ss = None
			se = None

			while True:
				meta_result = collect_repos.collect_repo_urls(token, cs, ce, True)	
				total_count =int(meta_result['total_count'])
				rate_limit = int(meta_result['rate_limit'])
				#if total_count <= 1000 and total_count >= 500:
				if total_count <= 1000 and total_count >= 500:
					break
				if total_count < 500:
					ss = cs
					se = ce
				if ss and se and (rate_limit <= 10):
					print 'Safety break to download less than 500'
					break
				if total_count == 0:
					initial_delta = timedelta(days=30)
				else:
					initial_delta = timedelta(math.floor(750/float(total_count)*initial_delta.days))
				if initial_delta == timedelta(0) and total_count > 1000:					
					ce = cs +timedelta(1)
					break				
				ce = cs + initial_delta

			if rate_limit <= 10 and ss and se:
				cs = ss
				ce = se

			meta_list_with_count = collect_repos.collect_repo_urls(token, cs, ce)
		meta_list = meta_list_with_count['meta_list']
		current_query_count = meta_list_with_count['total_count']
		total_num_of_repo_queried += current_query_count
				
			
		#Load from result file
		#with open(result_file_dir) as result_data:
		#	result_dict = json.load(result_data, encoding="latin-1")
		result_dict = {}
		#Create an initial dictionary to collect statistic such as user and repo names
		url_list = []
		for meta_info in meta_list:
			url = meta_info['url']
			created_at = meta_info['created_at']
			pushed_at = meta_info['pushed_at']
			size = meta_info['size']
			contributors_url = meta_info['contributors_url']
			url_list.append(url)
			items = url.split('/')
			username = items[-3]	
			reponame = items[-2]
			if not username in result_dict:
				#result_dict[items[-3]] = [{items[-2]:[]}]
				result_dict[username] = {reponame:{
									'files': [],
									'created_at': created_at,
									'pushed_at': pushed_at,
									'size': size,
									'contributors_url': contributors_url
									}}
			elif not reponame in result_dict[username]:
				#result_dict[items[-3]].append({items[-2]:[]})  
				result_dict[username][reponame] = { 
									'files': [],
									'created_at': created_at,
									'pushed_at': pushed_at,
									'size': size,
									'contributors_url': contributors_url
								 	}
			
		#print result_dict	

		current_num_download = len(url_list)	
		total_num_of_repo_downloaded += current_num_download
		print 'Downloading ' + str(current_num_download) + ' tar files'



		#download_repo.download_url(url_list[0], 0, token)
		#Cautions!!
		#The following code will download less than a thousand repos
		#download_repo.download_urls(url_list, token)
		
		#Uncomment the following line to unleash the beast
		start_time = time.time()	
		reponame_to_username = download_repo.download_urls(url_list, token)
		end_time = time.time()	
		elapsed_time = end_time - start_time
		total_seconds_of_download += elapsed_time
		print 'Time spent for downloading: ', elapsed_time

		#dict_dir = result_dir + '/' + 'repo_dict.out'
		############################################################################
		#save repo to user name for testing purpose	
		#with open(dict_dir, 'w') as dwrite:
		#	json.dump(reponame_to_username, dwrite)
		############################################################################
		#with open(dict_dir) as d_file:
		#	reponame_to_username = json.load(d_file)
		
		untar.untar_dir(data_dir)
		util.delete_tarballs(data_dir)
		all_c_files = util.find_extensions('.c', data_dir)
		print 'Total number of C files: ' + str(len(all_c_files))

		# result_dict_for_RE = result_dict
		start_time = time.time()	
		SA.parse(result_dir + "/results_rats.json", reponame_to_username, result_dict)
		
		#Check for files using the vulnerabilities list set up top 
		# results = check_file_vuls.scan_files_for_vul(data_dir, all_c_files, vulnerabilities + good_practices)
		end_time = time.time()	
		elapsed_time = end_time - start_time
		total_seconds_of_analyzing += elapsed_time
		#print results
		print 'Time spent for analyzing: ', elapsed_time


		#Update the initial result data with vulnerabilities of spefic files in each repo q
		# for entry in results:
		# 	for key, val in entry.iteritems():
		# 		#print key
		# 		first_idx = key.find('/')
		# 		unique_path = key[first_idx+1:]
		# 		key = key.split('/')
		# 		reponame = key[0]
		# 		last_idx = reponame.rfind('_')
		# 		reponame_no_underscore = reponame[:last_idx]
		# 		filename = key[-1]
		# 		#print reponame_no_underscore + " " + filename
		# 		#print reponame_to_username[reponame]
		# 		username = reponame_to_username[reponame]
		# 		#print result_dict[username]
		# 		result_dict[username][reponame_no_underscore]['files'].append({unique_path: val})
		# with open(result_dir + "/result_RE.json", 'w') as outfile:
			# json.dump(result_dict_for_RE, outfile, ensure_ascii=False)	
		
		# util.delete_in_directory(data_dir)

		#print result_dict
		#TODO delete all files after security analysis
		### commenting this out for now
		# import_json_to_db.import_to_database(result_dict, credentials_file)

		#saving the result
		result_with_date = {'start' : str(cs), 'end': str(ce), 'result': result_dict}
		with open(result_file_dir,'w') as outfile:	
			json.dump(result_with_date, outfile, ensure_ascii=False) 
		# analyze_json.collect_num_files_using_func(result_dict, 'gets')
		total_list = vulnerabilities + good_practices
		#num_list = analyze_json.collect_num_files_using_func_list(result_dict, total_list)
		#print total_list
		#print num_list
		if cs:
			ps = cs	
		pe = ce
		cs = ce
		initial_delta = max(initial_delta, timedelta(1))
		ce += initial_delta		
		print 'Previous start: ', ps,' Previous end: ',pe, ' Current start: ',cs, ' Current end: ',ce

	print 'total number of repo queried ', total_num_of_repo_queried 
	print 'total number of repo downloaded ', total_num_of_repo_downloaded 
	print 'total time spent for downloading ', total_seconds_of_download 
	print 'total time spent for querying ', total_seconds_of_analyzing 
	#sleep_time = 18
		#print 'Sleeping for ' + str(sleep_time) +'s ...'
		#time.sleep(sleep_time)
