import requests
import json
import time
from datetime import date, datetime, timedelta
from time import gmtime, time
import download_repo
import math
import util
#today = date.today()
#print today

language = 'PHP'
size_limit = '1000'
per_page = 100
compress_format = 'tarball'

#args = starting_date, ending_date(optional), page_num 
def collect_urls_by_page_num(token, page_num, starting_date=None, ending_date=None, counter_flag=False):
	if not starting_date:
		print 'Not enough args'
	if not ending_date:
		query_url = ("https://api.github.com/search/repositories?"
			     "q=language:"+language +
			     "+size:<=" + size_limit +
			     "+created:<="+str(starting_date) +
			     "&per_page=" + str(per_page) +
			     "&page=" + str(page_num)
			    )
	else:
		#TODO
		#Offset purpose
		starting_date += timedelta(days=1)
		query_url = ("https://api.github.com/search/repositories?"
			     "q=language:"+language +
			     "+size:<=" + size_limit +
			     "+created:"+str(starting_date) + ".." + str(ending_date) +
			     "&per_page=" + str(per_page) +
			     "&page=" + str(page_num)
			    )
	header = {'Authorization': 'token ' + str(token)}	

	#url_list = []	
	meta_list = []
	if counter_flag:
		print query_url
	if not token:
		r = requests.get(query_url)
	else:
		r = requests.get(query_url, headers=header)
	#print r.headers
	if(r.ok):
		#TODO:time to sleep
		#print 'Request for Page Num: ' + str(page_num) + ' returns OK'	
		#print 'Remaining request: ' + r.headers['x-ratelimit-remaining'] 
		#print ' date: ' + r.headers['date'] + ' reset: ' + datetime.utcfromtimestamp(int(r.headers['x-ratelimit-reset'])).isoformat() 
		#print str(r.headers['x-ratelimit-reset']) + ' ' + str(time())
		rate_remaining = r.headers['x-ratelimit-remaining']
		reset_time = int(r.headers['x-ratelimit-reset'])
		if rate_remaining == 0:
			 util.nap(reset_time)
		repoItem = json.loads(r.text or r.content)
		total_count = repoItem['total_count']
		repoList = repoItem['items']
		if counter_flag:
			return {'total_count': total_count, 'rate_limit': r.headers['x-ratelimit-remaining']}		
		#print len(repoItem)
		#Print it to see everything you mioght need from repo query, ask nina for pretty print
		#print repoItem
		#print len(repoItem['items'])
		for item in repoList:
			url = item['url'] + '/' + compress_format
			created_at = item['created_at']
			pushed_at = item['pushed_at']
			size = item['size']
			contributors_url = item['contributors_url']
			description = item['description']
			meta_list.append({
					'url': url,
					'created_at': created_at,
					'pushed_at': pushed_at,
					'size': size,
					'contributors_url': contributors_url,
					'description': description,
					'forks_url': item['forks_url'],
					'stargazers': item['stargazers_count'],
					'forks': item['forks_count'],
					'actual_url': item['html_url']
					})
	else:
		print 'Request for Page Num: ' + str(page_num) + ' ERROR'
		print r.headers	
		
	return {'total_count': total_count,'meta_list': meta_list}


def collect_repo_urls(token=None, starting_date=None, ending_date=None, counter_flag=False):
	if not starting_date:
		print 'Not enough arguments'
		return
	page_num = 1
	if not ending_date:
		#print str(starting_date)
		result =  collect_urls_by_page_num(token, page_num, starting_date)
	else:
		#print str(starting_date)
		if counter_flag:
			return  collect_urls_by_page_num(token, page_num, starting_date, ending_date, counter_flag)
		else:
			result =  collect_urls_by_page_num(token, page_num, starting_date, ending_date)

	total_count = result['total_count']
	meta_list = result['meta_list']
	#print total_count
	num_page = int(math.ceil(total_count/float(per_page)))
	num_page = min(num_page, 10)
	#print type(num_page)	
	#print num_page
	page_num += 1

	while page_num <= num_page:
		#print page_num
		if not ending_date:
			result =  collect_urls_by_page_num(token, page_num, starting_date)
		else:
			result =  collect_urls_by_page_num(token, page_num, starting_date, ending_date)
		meta_list += result['meta_list']		
		page_num += 1	
	return {
		'meta_list': meta_list,
		'total_count': int(total_count)
		}
	#&sort=created&order=asc
	#query_url = 'https://api.github.com/search/repositories?q=language:C+size:<=1000&per_page=100&page=10';
	#print repoList[0]

if __name__ == '__main__':
	download_repo.make_folder('../data')
	url_list = collect_repo_urls()
	#for url in url_list:
	download_repo.download_url(url_list[0])
	print url_list[0].split('/')[-2]
