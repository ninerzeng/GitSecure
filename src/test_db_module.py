import save_data as sd
import datetime

from imp import reload
reload(sd)

def test(credentials_file='mysqlcreds.csv'):
  con = sd.get_connection(credentials_file);
  username = "test_user"
  sd.save_user_data(con, username, "fake@email.com");
  
  #repo_id = save_repo_data("test_repo", date_created, user_id, repo_size, date_collected);
  #fill in with appropriate data types
  repo_id = sd.save_repo_data(con, "test_repo", datetime.date.today(), username, 2400, datetime.date.today());

  file_id = sd.save_file_data(con, "test_file.c", repo_id, "");

  #optional date and author parameters
  vuln_id = sd.save_vulnerability_data(con, file_id, 24, "code sample;");
  
  sd.close_connection(con);
