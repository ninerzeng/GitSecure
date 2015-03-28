import os
import untar
import download_repo
import collect_repos
from datetime import date

data_dir = '../data'
token = os.environ.get('P_TOKEN', None)

#Get folders prior to Jan 1st, 2009
starting_date = date(2009,1,1)
if __name__ == '__main__':
	if not token:
		print 'Forgot to export your token'
	#Create folder data if it does not exist already
	if not os.path.exists(data_dir):
		download_repo.make_folder(data_dir)
	url_list = collect_repos.collect_repo_urls(token, starting_date)	
	print 'Downloading ' + str(len(url_list)) + ' tar files'
	#download_repo.download_url(url_list[0], token)
	#Cautions!!
	#The following code will download less than a thousand repos
	download_repo.download_urls(url_list, token)
	#untar.untar_dir(data_dir)

