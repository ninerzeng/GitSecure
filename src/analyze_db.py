

#get number of distinct {repo, file, vuln} containing a particular vulnerability
"select count(distinct %s) 
from 
    gh_repo r
    inner join gh_file f on f.repo_id = r.repo_id
    inner join gh_vuln v on f.file_id = v.file_id
    where vuln_desc = %s", ("id_type {repo, file, vuln}", "vulnerability description")
