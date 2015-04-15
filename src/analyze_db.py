import save_data as sd
import csv
#from imp import reload
reload(sd)
import matplotlib.pyplot as plt
import datetime
import numpy as np

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

  db_conn = sd.get_connection("mysqlcreds-analysis.csv");
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
        print vuln_list[i], ", ", vuln_list[j], ", ", row[0], ", repos,", datetime.datetime.now()

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
        print vuln_list[i], ", ", alt_list[j], ", ", row[0], ", repos,", datetime.datetime.now()

#repos contributed to per user
#select username, count(distinct repo_id) from gh_repo_contributors group by username order by count(distinct repo_id);

def get_graphs_prepopulated():
  get_graphs(['strcpy', 'strcat', 'sprintf', 'vsprintf', 'gets', 'getpw'], ['strncpy', 'strncat', 'strlcpy', 'strlcat', 'snprintf', 'vsnprintf', 'fgets', 'getpwuid']);

def get_graphs(vuln_list, alt_list):
#  plt.plot(stuff)
#  plt.show()
# get number of users who have each number of different repos they contribute to
  db_conn = sd.get_connection("mysqlcreds-analysis.csv");
  #b(db_conn, vuln_list)
  #for vuln in vuln_list:
    #b(db_conn, [vuln])
  c1(db_conn, ["strcpy"], ["strncpy"])
  c1(db_conn, ["strcpy"], ["strlcpy"])
  
  rows = sd.select_many_query(db_conn, \
"select count(distinct username), repo_contribs from ( select username, count(distinct repo_id) repo_contribs from gh_repo_contributors group by username order by count(distinct repo_id) ) a group by repo_contribs");
  users = []
  repos_contributed_to = []
  for i in range(0, len(rows)):
    users.append(rows[i][0])
    repos_contributed_to.append(rows[i][1])
#  plt.plot(repos_contributed_to, users)
#  plt.show()
#contributors per repo
#select repo_id, count(distinct username) from gh_repo_contributors group by repo_id order by count(distinct username);

# get number of repos with each number of different contributors
  rows = sd.select_many_query(db_conn, \
"select count(distinct repo_id), num_contribs from ( select repo_id, count(distinct username) num_contribs from gh_repo_contributors group by repo_id order by count(distinct username) ) a group by num_contribs")

  #also correlation between repo size and vuln types/frequency
  #trends over time? not sure how to measure. maybe time last pushed
  #also correlation between number of contributors and vulnerability content

#okay, other analysis we'd like to do:
#ummmm....shit this is not going well
# we could look at the number of contributors vs. vuln count/vuln types - that would be a nice thing to graph
  #rows = sd.select_many_query(db_conn, \
  rows = sd.select_many_query(db_conn, \
"select r.repo_id, count(distinct rc.username), count(distinct v.vuln_id) \
from gh_repo r inner join \
gh_repo_contributors rc on r.repo_id = rc.repo_id \
inner join gh_file f on r.repo_id = f.repo_id \
inner join gh_vuln v on f.file_id = v.file_id \
where v.vuln_desc in (%s) \
group by r.repo_id \
", ['\'' + '\', \''.join(vuln_list) + '\''])



  #rows = sd.select_many_query(db_conn, \
  print \
"select r.repo_id, count(distinct rc.username), count(distinct v.vuln_desc) \
from gh_repo r inner join \
gh_repo_contributors rc on r.repo_id = rc.repo_id \
inner join gh_file f on r.repo_id = f.repo_id \
inner join gh_vuln v on f.file_id = v.file_id \
where v.vuln_desc in (%s) \
group by r.repo_id" % '\'' + '\', \''.join(vuln_list) + '\''
#group by r.repo_id", '\'' + '\', \''.join(vuln_list) + '\'')

# could look at proportion of repos a user contributes to that have vulns vs no-vulns

# create a view that has gh_vuln with the vulnerabilities, and another one that has the safe versions
  print \
"select rcv.username, count(distinct rcv.repo_id), count(distinct rcnv.repo_id) \
from gh_repo_contributors rcv \
inner join \
gh_repo_contributors rcnv on rcv.username = rcnv.username \
where rcnv.repo_id not in (select f.repo_id from gh_file f inner join gh_vuln v on f.file_id = v.vuln_id where v.vuln_desc in (%s)) \
and rcv.repo_id in (select f.repo_id from gh_file f inner join gh_vuln v on f.file_id = v.vuln_id where v.vuln_desc in (%s)) \
" % '\'' + '\', \''.join(vuln_list) + '\'', '\'' + '\', \''.join(vuln_list) + '\'' 





def a(db_conn, vuln_list):

  query_base = \
"select sum(vulns) / count(distinct repo_id) from \
(select r.repo_id, count(distinct rc.username), count(distinct v.vuln_id) vulns \
from gh_repo r inner join \
gh_repo_contributors rc on r.repo_id = rc.repo_id \
inner join gh_file f on r.repo_id = f.repo_id \
left join gh_vuln v on f.file_id = v.file_id \
where (v.vuln_desc in (" + '\'' + '\', \''.join(vuln_list) + '\'' + ") or v.vuln_desc is null)\
and r.repo_size >= %s and r.repo_size < %s \
group by r.repo_id "
  t1 = 5
  t2 = 10
  avg_vulns_under = []
  ra_under = []
  avg_vulns_mid = []
  ra_mid = []
  avg_vulns_over = []
  ra_over = []
  for i in range(0,1000,100):
    rows = sd.select_many_query(db_conn, query_base +\
" having count(distinct rc.username) <= %s) a", [i, i+100, t1])
    if rows[0]:
      ra_under.append(i);
      print "appending ", i
      avg_vulns_under.append(rows[0][0])
    
    rows = sd.select_many_query(db_conn, query_base +\
" having count(distinct rc.username) > %s \
and count(distinct rc.username) <= %s) a", [i, i+100, t1, t2])
    if rows[0]:
      ra_mid.append(i);
      print "appending ", i
      avg_vulns_mid.append(rows[0][0])
    
    rows = sd.select_many_query(db_conn, query_base +\
" having count(distinct rc.username) > %s) a", [i, i+100, t2])
    if rows[0]:
      ra_over.append(i);
      print "appending ", i
      avg_vulns_over.append(rows[0][0])
  l_under, = plt.plot(ra_under, avg_vulns_under, label="under " + str(t1) + ", ".join(vuln_list))
  l_mid, =  plt.plot(ra_mid, avg_vulns_mid, label="between " + str(t1) + " and " + str(t2) + ", ".join(vuln_list))
  l_over, = plt.plot(ra_over, avg_vulns_over, label="over " + str(t2) + ", ".join(vuln_list))
  plt.legend(handles=[l_under, l_mid, l_over])#, ["over", "under"])
  return [ra_under, avg_vulns_under, ra_mid, avg_vulns_mid, ra_over, avg_vulns_over , [l_under, l_mid, l_over]]
#axes: reported repo size on x axis, avg vulnerabilities on y axis

def b(db_conn, vuln_list):
  a(db_conn, vuln_list);
  plt.title(", ".join(vuln_list));
  plt.show()

def divide_non_zero(pair):
  if (pair[1] == 0 or pair[1] == None): 
    return 0; 
  else: 
    return pair[0]/pair[1]

def c(db_conn, vuln_list1, vuln_list2):
  [ra_under, avg_vulns_under, ra_mid, avg_vulns_mid, ra_over, avg_vulns_over , tmp] = a(db_conn, vuln_list1);
  [ra_under2, avg_vulns_under2, ra_mid2, avg_vulns_mid2, ra_over2, avg_vulns_over2 , tmp2] = a(db_conn, vuln_list2);
  plt.legend(handles=tmp + tmp2)
  plt.title(", ".join(vuln_list1) + ", " + ", ".join(vuln_list2));
  plt.show()

  vu = map( lambda pair: divide_non_zero(pair) , zip(avg_vulns_under, avg_vulns_under2))
  vm = map( lambda pair: divide_non_zero(pair) , zip(avg_vulns_mid, avg_vulns_mid2))
  vo = map( lambda pair: divide_non_zero(pair) , zip(avg_vulns_over, avg_vulns_over2))

#  vu = np.divide(avg_vulns_under, avg_vulns_under2)
#  vm = np.divide(avg_vulns_mid, avg_vulns_mid2)
#  vo = np.divide(avg_vulns_over, avg_vulns_over2)
  p1, = plt.plot(vu, label="under")
  p2, = plt.plot(vm, label="mid")
  p3, = plt.plot(vo, label="over")
  plt.legend(handles=[p1,p2,p3])
  plt.show()

def a1(db_conn, vuln_list):

  query_base = \
"select contribs, vulns from \
(select r.repo_id, count(distinct rc.username) contribs, count(distinct v.vuln_id) vulns \
from gh_repo r inner join \
gh_repo_contributors rc on r.repo_id = rc.repo_id \
inner join gh_file f on r.repo_id = f.repo_id \
left join gh_vuln v on f.file_id = v.file_id \
where (v.vuln_desc in (" + '\'' + '\', \''.join(vuln_list) + '\'' + ") or v.vuln_desc is null)\
and r.repo_size >= %s and r.repo_size < %s \
group by r.repo_id "
  t1 = 5
  t2 = 10
  avg_vulns_under = []
  std_dev_under = []
  ra_under = []
  avg_vulns_mid = []
  std_dev_mid = []
  ra_mid = []
  avg_vulns_over = []
  std_dev_over = []
  ra_over = []
  [uavg, ustddev, ux_axis] = execute_query_over_range(db_conn, query_base +\
" having count(distinct rc.username) <= %s) a", [t1])
  [mavg, mstddev, mx_axis] = execute_query_over_range(db_conn, query_base + " having count(distinct rc.username) > %s \
and count(distinct rc.username) <= %s) a", [t1, t2])
  [oavg, ostddev, ox_axis] = execute_query_over_range(db_conn, query_base +\
" having count(distinct rc.username) > %s) a", [t2])
  l_under, = plt.plot(ux_axis, uavg, label="under " + str(t1) + ", ".join(vuln_list))
  plt.errorbar(ux_axis, uavg, yerr=ustddev)
  l_mid, =  plt.plot(mx_axis, mavg, label="between " + str(t1) + " and " + str(t2) + ", ".join(vuln_list))
  l_over, = plt.plot(ox_axis, oavg, label="over " + str(t2) + ", ".join(vuln_list))
  plt.legend(handles=[l_under, l_mid, l_over])#, ["over", "under"])
  return [ux_axis, uavg, mx_axis, mavg, ox_axis, oavg, [l_under, l_mid, l_over]]
#axes: reported repo size on x axis, avg vulnerabilities on y axis

def b1(db_conn, vuln_list):
  a1(db_conn, vuln_list);
  plt.title(", ".join(vuln_list));
  plt.show()

def divide_non_zero(pair):
  if (pair[1] == 0 or pair[1] == None): 
    return 0; 
  else: 
    return pair[0]/pair[1]

def c1(db_conn, vuln_list1, vuln_list2):
  [ra_under, avg_vulns_under, ra_mid, avg_vulns_mid, ra_over, avg_vulns_over , tmp] = a1(db_conn, vuln_list1);
  [ra_under2, avg_vulns_under2, ra_mid2, avg_vulns_mid2, ra_over2, avg_vulns_over2 , tmp2] = a1(db_conn, vuln_list2);
  plt.legend(handles=tmp + tmp2)
  plt.title(", ".join(vuln_list1) + ", " + ", ".join(vuln_list2));
  plt.show()

  vu = map( lambda pair: divide_non_zero(pair) , zip(avg_vulns_under, avg_vulns_under2))
  vm = map( lambda pair: divide_non_zero(pair) , zip(avg_vulns_mid, avg_vulns_mid2))
  vo = map( lambda pair: divide_non_zero(pair) , zip(avg_vulns_over, avg_vulns_over2))

#  vu = np.divide(avg_vulns_under, avg_vulns_under2)
#  vm = np.divide(avg_vulns_mid, avg_vulns_mid2)
#  vo = np.divide(avg_vulns_over, avg_vulns_over2)
  p1, = plt.plot(vu, label="under")
  p2, = plt.plot(vm, label="mid")
  p3, = plt.plot(vo, label="over")
  plt.legend(handles=[p1,p2,p3])
  plt.show()


def execute_query_over_range(db_conn, query, args):
  avg = []
  stddev = []
  x_axis = []
  for i in range(0,1000,100):
    rows = sd.select_many_query(db_conn, query, [i, i+100] + args)
    #query_base + " having count(distinct rc.username) <= %s) a", args)#[i, i+100, t1])
    vulncount = []
    for row in rows:
      vulncount.append(row[1])
    avg.append(np.average(vulncount))
    stddev.append(np.std(vulncount))
    x_axis.append(i)
  print avg
  print stddev
  print x_axis
  return [avg, stddev, x_axis]
