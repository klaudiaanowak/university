-- Create tables
CREATE TABLE member(
login integer PRIMARY KEY,
password varchar(128) NOT NULL,
lastUpdate timestamp NOT NULL,
leader boolean NOT NULL);

CREATE TABLE authority(
id integer PRIMARY KEY);

CREATE TABLE project(
id integer PRIMARY KEY,
author integer NOT NULL REFERENCES member (login),
creationDate timestamp NOT NULL,
authority integer NOT NULL REFERENCES authority (id));

CREATE TABLE action(
id integer PRIMARY KEY,
type varchar(255) NOT NULL,
creationDate timestamp NOT NULL,
author integer NOT NULL REFERENCES member (login),
projectID integer NOT NULL REFERENCES project (id));

CREATE TABLE vote(
id SERIAL PRIMARY KEY,
member integer NOT NULL REFERENCES member (login),
action integer NOT NULL REFERENCES action (id),
type varchar(10) NOT NULL,
timestamp timestamp NOT NULL);

CREATE TABLE index(
id SERIAL PRIMARY KEY,
u_index integer NOT NULL	
);	
							   
-- Check if member exists and add new if not
CREATE FUNCTION add_member_if_not_exists(id integer, pass varchar(128), creation integer) RETURNS VOID
AS $X$
BEGIN
IF NOT EXISTS (SELECT member.login from member where member.login = id) 
THEN 
INSERT INTO member(login, password, lastUpdate, leader) VALUES (id, pass, to_timestamp(creation), false);																										   
END IF;																	  
END									   
$X$
LANGUAGE plpgsql;

-- Check if user get correct password											   
CREATE FUNCTION check_pass(id integer, pass varchar(128), isleader boolean[] ) RETURNS boolean 
AS $X$		
DECLARE p varchar(128);											   
BEGIN	
IF NOT EXISTS (SELECT * FROM member WHERE login = id and leader = ANY(isleader) and password = crypt(pass,member.password))								   
THEN RETURN False; ELSE RETURN True; 
END IF;						  								   
END											   
$X$
LANGUAGE plpgsql;
			 

-- Check if member was active earlier than year ago			 
CREATE FUNCTION check_active(id integer, newdate integer) RETURNS boolean 
AS $X$
DECLARE last_update timestamp;
DECLARE diff int;											   
BEGIN
SELECT lastUpdate FROM member WHERE login = id INTO last_update;
SELECT EXTRACT(YEAR from AGE(to_timestamp(newdate),last_update)) INTO diff;
IF (diff < 1) THEN RETURN True; ELSE RETURN False; 
END IF;						  								   
END											   
$X$
LANGUAGE plpgsql;	

-- 	Add new project oraz authority, if not exists						 
CREATE FUNCTION add_project_if_not_exists(new_project integer, member integer, creation integer, project_authority integer) RETURNS VOID
AS $X$
BEGIN
IF NOT EXISTS (SELECT project.id from project where project.id = new_project) 
THEN 
IF NOT EXISTS (SELECT authority.id from authority where authority.id = project_authority) 	
THEN 
INSERT INTO authority(id) VALUES (project_authority);	
END IF;											   
INSERT INTO project(id, author, creationDate, authority ) VALUES (new_project, member, to_timestamp(creation), project_authority);		
END IF;																	  
END									   
$X$
LANGUAGE plpgsql;	

-- Trigger before insert on vote - check if member voted for the action before			 
CREATE FUNCTION check_vote() RETURNS trigger
AS $X$
BEGIN
IF NOT EXISTS (SELECT * from action where id = new.action) 
THEN 
RETURN NULL;
ELSIF EXISTS (SELECT * from vote where member = new.member and action = new.action) 
THEN 
RETURN NULL;
ELSE
RETURN NEW;				 
END IF;																	  
END											   
$X$
LANGUAGE plpgsql;	

CREATE TRIGGER vote_bi_trigger BEFORE INSERT ON vote FOR EACH ROW EXECUTE PROCEDURE check_vote();			

-- Trigger before insert on action - check if project exists		 
CREATE FUNCTION check_project() RETURNS trigger
AS $X$
BEGIN
IF NOT EXISTS (SELECT * from project where id = new.projectid) OR  EXISTS (SELECT * from index where u_index = new.id)
THEN 
RETURN NULL;
ELSE
RETURN NEW;				 
END IF;																	  
END											   
$X$
LANGUAGE plpgsql;	

CREATE TRIGGER action_bi_trigger BEFORE INSERT ON action FOR EACH ROW EXECUTE PROCEDURE check_project();			
							 
							 
-- Trigger after insert on action - update last members's activity date							 
CREATE FUNCTION update_member() RETURNS trigger
AS $X$
BEGIN
UPDATE member SET lastUpdate = new.creationDate WHERE member.login = new.author;	
INSERT INTO index(u_index) VALUES (new.id); 							 
RETURN NEW;											   
END									   
$X$
LANGUAGE plpgsql;				

CREATE TRIGGER action_ai_trigger AFTER INSERT ON action FOR EACH ROW EXECUTE PROCEDURE update_member();			
	
-- Trigger after insert on votes - update last members's activity date							 
CREATE FUNCTION update_vote() RETURNS trigger
AS $X$
BEGIN
UPDATE member SET lastUpdate = new.timestamp WHERE member.login = new.member;	
RETURN NEW;											   
END									   
$X$
LANGUAGE plpgsql;				

CREATE TRIGGER vote_ai_trigger AFTER INSERT ON vote FOR EACH ROW EXECUTE PROCEDURE update_vote();	
							 
-- Trigger before insert on member - check index			 
CREATE FUNCTION check_member_index() RETURNS trigger
AS $X$
BEGIN
new.password = crypt(new.password,gen_salt('md5'));							 
IF EXISTS (SELECT * from index where u_index = new.login) 
THEN 
RETURN NULL;
ELSE
RETURN NEW;				 
END IF;																	  
END											   
$X$
LANGUAGE plpgsql;	

CREATE TRIGGER member_bi_trigger BEFORE INSERT ON member FOR EACH ROW EXECUTE PROCEDURE check_member_index();			

				 
-- Trigger after insert on member - add index					 
CREATE FUNCTION add_member_index() RETURNS trigger
AS $X$
BEGIN
INSERT INTO index(u_index) VALUES (new.login); 							 
RETURN NEW;											   
END									   
$X$
LANGUAGE plpgsql;				

CREATE TRIGGER member_ai_trigger AFTER INSERT ON member FOR EACH ROW EXECUTE PROCEDURE add_member_index();		
							 
-- Trigger before insert on project - check index			 
CREATE FUNCTION check_project_index() RETURNS trigger
AS $X$
BEGIN
IF EXISTS (SELECT * from index where u_index = new.id) 
THEN 
RETURN NULL;
ELSE
RETURN NEW;				 
END IF;																	  
END											   
$X$
LANGUAGE plpgsql;	

CREATE TRIGGER project_bi_trigger BEFORE INSERT ON project FOR EACH ROW EXECUTE PROCEDURE check_project_index();			

				 
-- Trigger after insert on project - add index					 
CREATE FUNCTION add_project_index() RETURNS trigger
AS $X$
BEGIN
INSERT INTO index(u_index) VALUES (new.id); 							 
RETURN NEW;											   
END									   
$X$
LANGUAGE plpgsql;				

CREATE TRIGGER project_ai_trigger AFTER INSERT ON project FOR EACH ROW EXECUTE PROCEDURE add_project_index();						 

-- Create View to trolls function
CREATE VIEW trolls_view AS
select member.login, count(nullif(vote.type,'downvote'))as upvotes, count(nullif(vote.type,'upvote')) as downvotes, member.lastUpdate
from member join action on (member.login = action.author) join vote on(action.id = vote.action) group by member.login;																				 
										   
-- Create user and give priviliges											   
CREATE USER app with encrypted password 'qwerty';
GRANT SELECT,INSERT,UPDATE ON ALL TABLES IN SCHEMA public TO app;
GRANT USAGE, SELECT ON SEQUENCE vote_id_seq TO app;	
GRANT USAGE, SELECT ON SEQUENCE index_id_seq TO app;								 