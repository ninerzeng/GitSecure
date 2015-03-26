import os
import download_repo
import collect_repos
from datetime import date

#Get folders prior to Jan 1st, 2009
starting_date = date(2009,1,1)
if __name__ == '__main__':
	#Create folder data if it does not exist already
	if not os.path.exists('../data'):
		download_repo.make_folder('../data')
	url_list = collect_repos.collect_repo_urls(starting_date)	
	print 'Downloading ' + str(len(url_list)) + ' tar files'
	#download_repo.download_url(url_list[0])
	#Cautions!!
	#The following code will download less than a thousand repos
	download_repo.download_urls(url_list)
	

