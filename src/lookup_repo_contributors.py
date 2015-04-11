import save_data as sd
import requests
import json
import util
import sys

in_order = True;

db_conn = sd.get_connection(credentials_file='mysqlcreds-remote.csv')
rows = None;
if (in_order):
	rows = sd.select_many_query(db_conn, "select repo_id, contributors_url, owner_name from gh_repo where repo_id >= (select coalesce(max(repo_id), 0) from gh_repo_contributors) order by repo_id")
else: #get the stragglers
	rows = sd.select_many_query(db_conn, "select repo_id, contributors_url, owner_name from gh_repo where repo_id not in (select repo_id from gh_repo_contributors) order by repo_id")

header = {'Authorization': 'token ' + '7ad044b7c036e7eca299cdea799a7b5bae093e26'}

for row in rows:
	repo_id = row[0];
	if (repo_id % 10 == 0):
		print "repo_id ", repo_id
	query_url = row[1];
	owner_name = row[2];
	try:
		r = requests.get(query_url, headers=header)
		item = json.loads(r.text or r.content)
		for thing in item:
			contributions = thing['contributions']
			username = thing['login']
			sd.save_user_data(db_conn, username);
			sd.save_repo_contributor_data(db_conn, username, repo_id, contributions);
		headers = r.headers;
		ratelimit_remaining = int(headers['x-ratelimit-remaining'])
		reset_time = int(headers['x-ratelimit-reset'])
		if (ratelimit_remaining % 10 == 0):
			print "ratelimit_remaining ", ratelimit_remaining
		if ratelimit_remaining == 0: 
			print "napping for ", reset_time
			util.nap(reset_time)
	except ValueError, ConnectionError:
		print "error: ", sys.exc_info()[0]
		print "skipping repo: ", repo_id
