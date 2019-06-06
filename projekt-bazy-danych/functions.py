import json
import datetime

def leader(timestamp, password, member, connection):
    try:
        sql = "INSERT INTO member(login,password,lastUpdate,leader) VALUES ({}, '{}', '{}', {})"
        cursor = connection.cursor()
        cursor.execute(sql.format(member, password, datetime.datetime.fromtimestamp(timestamp), True))
        connection.commit()
        return(json.dumps({"status": "OK"}))
    except:
        return(json.dumps({"status": "ERROR"}))


def protest(timestamp, password, member, action, project, authority,connection):
    # sprawdza poprawność hasła
    # dodaje członka jeśli nie istnieje
    # dodaje projekt / authority jeśli nie istnieje
    # trigger after insert do aktualizacji last update member
    try:
        check_member = "SELECT add_member_if_not_exists({},'{}',{})"
        check_project = "SELECT add_project_if_not_exists({}, {}, {}, {})"
        sql = "INSERT INTO action(id, type, creationDate, author, projectID) VALUES ({}, '{}', '{}', {}, {})"
        cursor = connection.cursor()
        cursor.execute(check_member.format(member,password,timestamp))
        cursor.execute(check_project.format(project,member,timestamp,authority))
        cursor.execute(sql.format(action, 'protest', datetime.datetime.fromtimestamp(timestamp), member, project))
        connection.commit()
        return(json.dumps({"status": "OK"}))
    except:
        return(json.dumps({"status": "ERROR"}))

    
def support(timestamp, password, member, action, project, authority,connection):
    try:
        check_member = "SELECT add_member_if_not_exists({},'{}',{})"
        check_project = "SELECT add_project_if_not_exists({}, {}, {}, {})"
        sql = "INSERT INTO action(id, type, creationDate, author, projectID) VALUES ({}, '{}', '{}', {}, {})"
        cursor = connection.cursor()
        cursor.execute(check_member.format(member,password,timestamp))
        cursor.execute(check_project.format(project,member,timestamp,authority))
        cursor.execute(sql.format(action, 'support', datetime.datetime.fromtimestamp(timestamp), member, project))
        connection.commit()
        return(json.dumps({"status": "OK"}))
    except:
        return(json.dumps({"status": "ERROR"}))


def upvote(timestamp, password, member, action, connection):
    try:
        sql = "INSERT INTO vote(member, action, type, timestamp) VALUES ({}, {}, '{}', {})"
        cursor = connection.cursor()
        cursor.execute(sql.format(member, action, 'upvote', datetime.datetime.fromtimestamp(timestamp)))
        connection.commit()
        return(json.dumps({"status": "OK"}))
    except:
        return(json.dumps({"status": "ERROR"}))
    
def downvote(timestamp, password, member, action, connection):
    try:
        sql = "INSERT INTO vote(member, action, type, timestamp) VALUES ({}, {}, '{}', {})"
        cursor = connection.cursor()
        cursor.execute(sql.format(member, action, 'udownvote', datetime.datetime.fromtimestamp(timestamp)))
        connection.commit()
        return(json.dumps({"status": "OK"}))
    except:
        return(json.dumps({"status": "ERROR"}))
    
{ "open": { "database": "student", "login": "init", "password": "qwerty"}}
{ "leader": { "timestamp": 1557473000, "password": "abc", "member": 1}}
{ "leader": { "timestamp": 1557474000, "password": "asd", "member": 2}}
{ "leader": { "timestamp": 1557474000, "password": "asd", "member": 3}}

{ "open": { "database": "student", "login": "app", "password": "qwerty"}}
{ "protest": { "timestamp": 1557475723, "password": "123", "member": 4, "action":11000, "project":6000, "authority":10000}}
{ "support": { "timestamp": 1557475701, "password": "123", "member": 30, "action":61000, "project":5000, "authority":10000}}
{ "upvote": { "timestamp": 1557475702, "password": "asd", "member": 2, "action":500}}
{ "downvote": { "timestamp": 1557475703, "password": "abc", "member": 1, "action":500}}
{ "downvote": { "timestamp": 1557475704, "password": "abc", "member": 1, "action":600}}
{ "votes": { "timestamp": 1557475705, "password": "abc", "member": 1}}
{ "trolls": { "timestamp": 1557477055 }}

