import MySQLdb as mdb
import sys
import csv
con = None

def get_connection(credentials_file='mysqlcreds.csv'):     
    with open(credentials_file, 'rb') as inputfile:
      inputreader = csv.DictReader(inputfile, delimiter=',')
      row = next(inputreader);
    try:
      con = mdb.connect(row['host'], row['user'], row['password'], row['database']);
    except mdb.Error, e: 
      print "Error %d: %s" % (e.args[0],e.args[1])
      if con:    
        con.close()            
      sys.exit(1)
    return con

def save_user_data(con, username, email=''):
    # if we encounter a user a second time, use insert ignore syntax to avoid inserting them a second time
    return execute_query(con, "insert ignore into gh_user (username, email) values (%s, %s)", (username, email));
    
def save_repo_data(con, repo_name, date_created, owner_name, repo_size, last_pushed, contributors_url=""):
    repo_id = execute_query(con, "insert ignore into gh_repo (repo_name, date_created, owner_name, repo_size, last_pushed, contributors_url) values (%s, %s, %s, %s, %s, %s)", (repo_name, date_created, owner_name, repo_size, last_pushed, contributors_url));
    if (repo_id == -1):
      repo_id = select_id_query(con, "select repo_id from gh_repo where repo_name = %s and owner_name = %s", (repo_name, owner_name));
    return repo_id

def save_repo_contributor_data(con, username, repo_id):
    return execute_query(con, "insert ignore into gh_repo_contributors (username, repo_id) values (%s, %s)", (username, repo_id));

def save_file_data(con, filename, repo_id, file_hash):
    file_id = execute_query(con, "insert ignore into gh_file (filename, repo_id, file_hash) values (%s, %s, %s)", (filename, repo_id, file_hash));
    if (file_id == -1):
      file_id = select_id_query(con, "select file_id from gh_file where filename = %s and repo_id = %s", (filename, repo_id));
    return file_id

def save_vulnerability_data(con, file_id, line_number, code_sample, vuln_desc, date_written='', author_name=''):
    vuln_id = execute_query(con, "insert into gh_vuln (file_id, line_number, code_sample, vuln_desc, date_written, author_name) values (%s, %s, %s, %s, %s, %s)", (file_id, line_number, code_sample, vuln_desc, date_written, author_name));
    # TODO: this currently cannot detect duplicate vulnerabilities
    return vuln_id

def execute_query(con, query, data):  
    if not con:
      print "Error: no database connection"
      sys.exit(1)
    # if this fails it should exit
    cursor = con.cursor();
    #print "executing insert query"
    try: 
        cursor.execute(query, data);
    except mdb.Error, e: 
        print "Error %d: %s" % (e.args[0],e.args[1])
        if con:    
            con.close()            
        sys.exit(1)
 
    lastrow = cursor.lastrowid;
    #print 'Last row id = ' + str(lastrow);
    if not cursor.lastrowid:
        #print('last insert id not found.')
        lastrow = -1;
    cursor.close();
    con.commit();
    return lastrow;
 
def select_id_query(con, query, data):  
    if not con:
      print "Error: no database connection"
      sys.exit(1)
    # if this fails it should exit
    cursor = con.cursor();
    #print "executing select query"
    try: 
        cursor.execute(query, data);
    except mdb.Error, e: 
        print "Error %d: %s" % (e.args[0],e.args[1])
        if con:    
            con.close()            
        sys.exit(1)
 
    #TODO: error handling here in case fetchone() fails
    row_id = cursor.fetchone()[0];
    #print 'Row id = ' + str(row_id);
    cursor.close();
    return row_id;

def select_many_query(con, query, data=None):  
    if not con:
      print "Error: no database connection"
      sys.exit(1)
    cursor = con.cursor();
    try: 
        cursor.execute(query, data);
    except mdb.Error, e: 
        print "Error %d: %s" % (e.args[0],e.args[1])
        if con:    
            con.close()            
        sys.exit(1)
    print cursor._last_executed 
    rows = cursor.fetchall();
    cursor.close();
    return rows;

def close_connection(con):
    con.close();
