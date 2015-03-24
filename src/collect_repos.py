import requests
import json

#&sort=created&order=asc
query_url = 'https://api.github.com/search/repositories?q=language:C+size:<=1000&per_page=100&page=10';
r = requests.get(query_url)
print r.headers
if(r.ok):
	repoItem = json.loads(r.text or r.content)
	print len(repoItem)
	#print repoItem
	print len(repoItem['items'])
	for item in repoItem['items']:
		print item