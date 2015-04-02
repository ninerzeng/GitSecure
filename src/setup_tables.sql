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
	date_collected datetime,
	repo_id int not null auto_increment, 
	primary key (repo_id),
	foreign key (owner_name) references gh_user(username),
	unique key (repo_name, owner_name)
);

create table gh_file (
	filename varchar(1000),
	repo_id int,
	file_hash varchar(1000),
	file_id int not null auto_increment, 
	primary key (file_id),
	foreign key (repo_id) references gh_repo(repo_id)
);

create table gh_vuln (
	vuln_id int not null auto_increment,
	line_number int, -- should we have an optional end line number?
	code_sample varchar(5000),
	file_id int,
	date_written datetime, -- may not be able to get this field
	author_name varchar(256), -- may not be able to get this field either
	primary key (vuln_id),
	foreign key (file_id) references gh_file(file_id)
)
