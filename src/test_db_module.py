import save_data as sd
import datetime

def test(credentials_file='mysqlcreds.csv'):
	get_connection(credentials_file);
	user_id = sd.save_user_data("test_user", "fake@email.com");
	
	#repo_id = save_repo_data("test_repo", date_created, user_id, repo_size, date_collected);
	#fill in with appropriate data types
	repo_id = sd.save_repo_data("test_repo", datetime.date.today(), user_id, 2400, datetime.date.today());

	file_id = sd.save_file_data("test_file.c", repo_id, "");

	#optional date and author parameters
	vuln_id = sd.save_vulnerability_data(file_id, 24, "code sample;");
	
	sd.close_connection();
