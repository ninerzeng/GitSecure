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
    #return user_id
    
def save_repo_data(con, repo_name, date_created, owner_name, repo_size, date_collected):
    return execute_query(con, "insert into gh_repo (repo_name, date_created, owner_name, repo_size, date_collected) values (%s, %s, %s, %s, %s)", (repo_name, date_created, owner_name, repo_size, date_collected));
    #return repo_id

def save_file_data(con, filename, repo_id, file_hash):
    return execute_query(con, "insert into gh_file (filename, repo_id, file_hash) values (%s, %s, %s)", (filename, repo_id, file_hash));
   # return file_id

def save_vulnerability_data(con, file_id, line_number, code_sample, date_written='', author_name=''):
    return execute_query(con, "insert into gh_vuln (file_id, line_number, code_sample, date_written, author_name) values (%s, %s, %s, %s, %s)", (file_id, line_number, code_sample, date_written, author_name));
   # return vuln_id

def execute_query(con, query, data):  
    if not con:
      print "Error: no database connection"
      sys.exit(1)
    # if this fails it should exit
    cursor = con.cursor();
    print "about to execute query"
    try: 
        cursor.execute(query, data);
    except mdb.Error, e: 
        print "Error %d: %s" % (e.args[0],e.args[1])
        if con:    
            con.close()            
        sys.exit(1)
 
    lastrow = cursor.lastrowid;
    print 'Last row id = ' + str(lastrow);
    if not cursor.lastrowid:
        print('last insert id not found.')
    cursor.close();
    con.commit();
    return lastrow;
 
def close_connection(con):
    con.close();
