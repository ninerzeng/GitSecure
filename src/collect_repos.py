import requests
import json
import time
from datetime import date
import download_repo
#today = date.today()
#print today
def collect_repo_urls():
	language = 'C'
	size_limit = '1000'
	starting_date = date(2009,1,1)
	per_page = 100
	page_num = 1
	compress_format = 'tarball'

	url_list = []
	print str(starting_date)



	#&sort=created&order=asc
	#query_url = 'https://api.github.com/search/repositories?q=language:C+size:<=1000&per_page=100&page=10';
	query_url = ("https://api.github.com/search/repositories?"
		     "q=language:"+language +
		     "+size:<=" + size_limit +
		     "+created:<"+str(starting_date) +
		     "&per_page=" + str(per_page) +
		     "&page=" + str(page_num)
		    )
	print query_url
	r = requests.get(query_url)
	print r.headers
	if(r.ok):
		repoItem = json.loads(r.text or r.content)
		repoList = repoItem['items']
		print len(repoItem)
		#print repoItem
		print len(repoItem['items'])
		for item in repoList:
	#		print item['url']
			url = item['url'] + '/' + compress_format
	#		print url
			url_list.append(url)
	#		print item
	return url_list
	#print repoList[0]

if __name__ == '__main__':
	download_repo.make_folder('../data')
	url_list = collect_repo_urls()
	#for url in url_list:
	download_repo.download_url(url_list[0])
	print url_list[0].split('/')[-2]
