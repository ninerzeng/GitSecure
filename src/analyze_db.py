
import save_data as sd
import csv
from imp import reload
reload(sd)

def get_analysis_prepopulated(output_filename):
  get_analysis(output_filename, ['strcpy', 'strcat', 'sprintf', 'vsprintf', 'gets', 'getpw'], ['strncpy', 'strncat', 'strlcpy', 'strlcat', 'snprintf', 'vsnprintf', 'fgets', 'getpwuid']);

def get_analysis(output_filename, vuln_list, alt_list):
  # get database connection (local for now)
  outfile = open(output_filename, "wb");
  id_types = ["r.repo_id", "f.file_id", "v.vuln_id"]
  id_names = ["number of repos", "number of files", "total occurrences"]
  fieldnames = ["vulnerability"] + id_names
  writer = csv.DictWriter(outfile, fieldnames=fieldnames);
  writer.writeheader();

  db_conn = sd.get_connection("mysqlcreds-throwaway.csv");
  for vuln in vuln_list:
    tmp_result = {"vulnerability": vuln};
    for i in range(0, len(id_types)):
#get number of distinct {repo, file, vuln} containing a particular vulnerability
#don't escape the id type
      rows = sd.select_many_query(db_conn, \
" select count(distinct " + id_types[i] + ")  \
 from \
   gh_repo r  \
   inner join gh_file f on f.repo_id = r.repo_id  \
   inner join gh_vuln v on f.file_id = v.file_id  \
   where vuln_desc = %s", [vuln]);
      for row in rows:
        tmp_result[id_names[i]] = row[0];
        #writer.writerow([ id_names[i], vuln, row[0] ]);
    writer.writerow(tmp_result)

  #Next, we'll want to look into co-occurrence of different types of vulnerabilities
  for i in range(0, len(vuln_list)):
    for j in range(i+1, len(vuln_list)):
      rows = sd.select_many_query(db_conn, \
"  select count(distinct r.repo_id) \
  from gh_repo r \
  inner join gh_file f1 on r.repo_id = f1.repo_id \
  inner join gh_vuln v1 on f1.file_id = v1.file_id \
  inner join gh_file f2 on r.repo_id = f2.repo_id \
  inner join gh_vuln v2 on f2.file_id = v2.file_id \
  and v1.vuln_desc = %s \
  and v2.vuln_desc = %s ", [vuln_list[i], vuln_list[j]]);
      for row in rows:
        print vuln_list[i], " occurs with ", vuln_list[j], " in ", row[0], " repos"

  #Also co-occurrence of unsafe and safe versions of functions
  for i in range(0, len(vuln_list)):
    for j in range(0, len(alt_list)):
      rows = sd.select_many_query(db_conn, \
"  select count(distinct r.repo_id) \
  from gh_repo r \
  inner join gh_file f1 on r.repo_id = f1.repo_id \
  inner join gh_vuln v1 on f1.file_id = v1.file_id \
  inner join gh_file f2 on r.repo_id = f2.repo_id \
  inner join gh_vuln v2 on f2.file_id = v2.file_id \
  and v1.vuln_desc = %s \
  and v2.vuln_desc = %s ", [vuln_list[i], alt_list[j]]);
      for row in rows:
        print vuln_list[i], " occurs with ", alt_list[j], " in ", row[0], " repos"

#repos contributed to per user
#select username, count(distinct repo_id) from gh_repo_contributors group by username order by count(distinct repo_id);

# get number of users who have each number of different repos they contribute to
select count(distinct username), repo_contribs from ( select username, count(distinct repo_id) repo_contribs from gh_repo_contributors group by username order by count(distinct repo_id) ) group by repo_contribs

#contributors per repo
#select repo_id, count(distinct username) from gh_repo_contributors group by repo_id order by count(distinct username);

# get number of repos with each number of different contributors
select count(distinct repo_id), num_contribs from ( select repo_id, count(distinct username) from gh_repo_contributors group by repo_id order by count(distinct username) ) group by num_contribs

  #also correlation between repo size and vuln types/frequency
  #trends over time? not sure how to measure. maybe time last pushed
  #also correlation between number of contributors and vulnerability content


#okay, other analysis we'd like to do:

