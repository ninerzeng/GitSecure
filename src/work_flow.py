import os
import download_repo
import collect_repos
from datetime import date

starting_date = date(2009,1,1)
if __name__ == '__main__':
	if not os.path.exists('../data'):
		download_repo.make_folder('../data')
	url_list = collect_repos.collect_repo_urls(starting_date)	
	download_repo.download_url(url_list[0])
	

