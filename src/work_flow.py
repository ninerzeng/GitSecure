import os
import untar
import util
import json
import download_repo
import collect_repos
from datetime import date

data_dir = '../data'
result_dir = '../result'
result_file = 'result.json'
token = os.environ.get('P_TOKEN', None)

#Get folders prior to Jan 1st, 2009
starting_date = date(2009,1,1)
if __name__ == '__main__':
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
	print result_dict
	#for url in url_list:
		

	print 'Downloading ' + str(len(url_list)) + ' tar files'



	download_repo.download_url(url_list[0], 0, token)
	#Cautions!!
	#The following code will download less than a thousand repos
	#download_repo.download_urls(url_list, token)
	#untar.untar_dir(data_dir)
