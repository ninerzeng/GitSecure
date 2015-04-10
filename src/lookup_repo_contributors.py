import save_data as sd
import requests
import json

db_conn = sd.get_connection(credentials_file='mysqlcreds-throwaway.csv')
rows = sd.select_many_query(db_conn, "select repo_id, contributors_url, owner_name from gh_repo where repo_id >= (select coalesce(max(repo_id), 0) from gh_repo_contributors) order by repo_id")

header = {'Authorization': 'token ' + '4e3197881d4c26d4b569a9ed1a5e418e04fbcebb'}

for row in rows:
  #lookup 
  repo_id = row[0];
  query_url = row[1];
  owner_name = row[2];
  #print query_url
  r = requests.get(query_url, headers=header)
  item = json.loads(r.text or r.content)
  for thing in item:
    contributions = thing['contributions']
    username = thing['login']
    sd.save_user_data(db_conn, username);
    sd.save_repo_contributor_data(db_conn, username, repo_id, contributions);
