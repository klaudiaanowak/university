CREATE USER app with encrypted password 'qwerty';
GRANT SELECT, INSERT, UPDATE, DELETE  ON ALL TABLES IN SCHEMA public TO app;

CREATE TABLE member(
login integer PRIMARY KEY,
password varchar(128),
lastUpdate timestamp,
leader boolean);

CREATE TABLE authority(
id integer PRIMARY KEY);

CREATE TABLE project(
id integer PRIMARY KEY,
author integer REFERENCES member (login),
creationDate timestamp,
authority integer REFERENCES authority (id));

CREATE TABLE action(
id integer PRIMARY KEY,
type varchar(255),
creationDate timestamp,
author integer REFERENCES member (login),
projectID integer REFERENCES project (id));

CREATE TABLE vote(
id integer PRIMARY KEY,
member integer REFERENCES member (login),
action integer REFERENCES action (id),
type varchar(10),
timestamp timestamp);
