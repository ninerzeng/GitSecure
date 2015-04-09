
import save_data as sd
import csv
from imp import reload
reload(sd)

def get_analysis(output_filename, vuln_list):
  # get database connection (local for now)
  outfile = open(output_filename, "wb");
  id_types = ["r.repo_id", "f.file_id", "v.vuln_id"]
  id_names = ["number of repos", "number of files", "total occurrences"]
  fieldnames = ["vulnerability"] + id_names
  writer = csv.DictWriter(outfile, fieldnames=fieldnames);
  writer.writeheader();

  db_conn = sd.get_connection("mysqlcreds-local.csv");
  for vuln in vuln_list:
    tmp_result = {"vulnerability": vuln};
    for i in range(0, len(id_types)):
#get number of distinct {repo, file, vuln} containing a particular vulnerability
#don't escape the id type
      rows = sd.select_many_query(db_conn, \
" select count(distinct " + id_types[i] + ") " + \
" from " + \
"   gh_repo r " + \
"   inner join gh_file f on f.repo_id = r.repo_id " + \
"   inner join gh_vuln v on f.file_id = v.file_id " + \
"   where vuln_desc = %s", [vuln]);
      for row in rows:
        tmp_result[id_names[i]] = row[0];
        #writer.writerow([ id_names[i], vuln, row[0] ]);
    writer.writerow(tmp_result)

  #Next, we'll want to look into co-occurrence of different types of vulnerabilities
  select count(distinct repo_id) 
  from gh_repo r
  inner join gh_file f1 on r.repo_id = f1.repo_id
  inner join gh_vuln v1 on f1.file_id = v1.file_id
  inner join gh_file f2 on r.repo_id = f2.repo_id
  inner going gh_vuln v2 on f2.file_id = v2.file_id
  where v1.vuln_desc <> v2.vuln_desc


  #Also co-occurrence of unsafe and safe versions of functions
  #also correlation between repo size and vuln types/frequency
  #trends over time? not sure how to measure. maybe time last pushed
  #also correlation between number of contributors and vulnerability content
