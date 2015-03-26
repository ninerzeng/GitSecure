import requests
import json
import time
from datetime import date
import download_repo
import math
#today = date.today()
#print today

language = 'C'
size_limit = '1000'
per_page = 100
compress_format = 'tarball'

#args = starting_date, ending_date(optional), page_num 
def collect_urls_by_page_num(*args):
	if len(args) == 2:
		starting_date = args[0]
		page_num = args[1]
		query_url = ("https://api.github.com/search/repositories?"
			     "q=language:"+language +
			     "+size:<=" + size_limit +
			     "+created:<"+str(starting_date) +
			     "&per_page=" + str(per_page) +
			     "&page=" + str(page_num)
			    )
	elif len(args) == 3:
		starting_date = args[0]
		ending_date = args[1]
		page_num = args[2]
		#TODO
	
	url_list = []	
	#print query_url
	r = requests.get(query_url)
	#print r.headers
	if(r.ok):
		print 'Request for Page Num: ' + str(page_num) + ' returns OK'	
		print 'Remaining request: ' + r.headers['x-ratelimit-remaining']
		repoItem = json.loads(r.text or r.content)
		total_count = repoItem['total_count']
		repoList = repoItem['items']
		#print len(repoItem)
		#print repoItem
		#print len(repoItem['items'])
		for item in repoList:
			url = item['url'] + '/' + compress_format
			url_list.append(url)
	else:
		print 'Request for Page Num: ' + str(page_num) + ' ERROR'
		print r.headers	
		
	return {'total_count': total_count,'url_list': url_list}


def collect_repo_urls(*args):

	if len(args) >= 1:
		starting_date = args[0]
		#print str(starting_date)
		page_num = 1
		result =  collect_urls_by_page_num(starting_date, 1)
		total_count = result['total_count']
		url_list = result['url_list']
		#print total_count
		num_page = int(math.ceil(total_count/float(per_page)))
		#print type(num_page)	
		#print num_page
		page_num += 1
		while page_num <= num_page:
			#print page_num
			result =  collect_urls_by_page_num(starting_date, page_num)
			url_list += result['url_list']		
			page_num += 1	
		return url_list
	#&sort=created&order=asc
	#query_url = 'https://api.github.com/search/repositories?q=language:C+size:<=1000&per_page=100&page=10';
	#print repoList[0]

if __name__ == '__main__':
	download_repo.make_folder('../data')
	url_list = collect_repo_urls()
	#for url in url_list:
	download_repo.download_url(url_list[0])
	print url_list[0].split('/')[-2]
