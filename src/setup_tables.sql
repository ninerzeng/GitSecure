create table gh_user (
	username varchar(256),
	email varchar(256),
	primary key (username)
);

create table gh_repo (
	repo_name varchar(256),
	date_created datetime,
	owner_name varchar(256),
	repo_size int,
	last_pushed datetime,
	url varchar(256),
	forks_url varchar(256),
	contributors_url varchar(256),
	description varchar(256),
	stargazers int,
	forks int,
	repo_id int not null auto_increment, 
	primary key (repo_id),
	foreign key (owner_name) references gh_user(username),
	unique key (repo_name, owner_name)
);

create table gh_repo_contributors (
  repo_id int,
  username varchar(256),
  contributions int,
  foreign key (repo_id) references gh_repo(repo_id),
  foreign key (username) references gh_user(username),
  unique key(repo_id, username)
);

create table gh_file (
	filename varchar(512),
	repo_id int,
	file_hash varchar(512),
	file_id int not null auto_increment, 
	primary key (file_id),
	foreign key (repo_id) references gh_repo(repo_id),
	unique key (filename, repo_id)
);

create table gh_vuln (
	vuln_id int not null auto_increment,
	line_number int, -- should we have an optional end line number?
	code_sample varchar(2048),
	vuln_desc varchar (512),
	file_id int,
	date_written datetime, -- may not be able to get this field
	author_name varchar(256), -- may not be able to get this field either
	primary key (vuln_id),
	foreign key (file_id) references gh_file(file_id),
	unique key (file_id, line_number)
);

create index vuln_descript on gh_vuln (vuln_desc);
