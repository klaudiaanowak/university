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
SELECT password FROM member WHERE login = id and leader = ANY(isleader)	INTO p;									   
IF (p IS NULL OR pass <> p ) THEN RETURN False; ELSE RETURN True; 
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
IF NOT EXISTS (SELECT * from project where id = new.projectid)
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
				 
							 
							 
-- Create user and give priviliges											   
CREATE USER app with encrypted password 'qwerty';
GRANT SELECT,INSERT,UPDATE ON ALL TABLES IN SCHEMA public TO app;
GRANT USAGE, SELECT ON SEQUENCE vote_id_seq TO app;											   						   