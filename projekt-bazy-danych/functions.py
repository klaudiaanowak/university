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
    #TODO sprawdz poprawność hasła
    #     utwórz trigger before insert
    try:
        sql = "INSERT INTO action(id, type, creationDate, author, projectID) VALUES ({}, '{}', '{}', {}, {})"
        cursor = connection.cursor()
        cursor.execute(sql.format(action, 'protest', datetime.datetime.fromtimestamp(timestamp), member, project))
        connection.commit()
        return(json.dumps({"status": "OK"}))
    except:
        return(json.dumps({"status": "ERROR"}))    

    
def support(timestamp, password, member, action, project, authority,connection):
    try:
        sql = "INSERT INTO action(id, type, creationDate, author, projectID) VALUES ({}, '{}', '{}', {}, {})"
        cursor = connection.cursor()
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

{ "open": { "database": "student", "login": "app", "password": "qwerty"}}
{ "protest": { "timestamp": 1557475700, "password": "123", "member": 2, "action":500, "project":5000, "authority":10000}}
{ "support": { "timestamp": 1557475701, "password": "123", "member": 3, "action":600, "project":5000}}
{ "upvote": { "timestamp": 1557475702, "password": "asd", "member": 2, "action":500}}
{ "downvote": { "timestamp": 1557475703, "password": "abc", "member": 1, "action":500}}
{ "downvote": { "timestamp": 1557475704, "password": "abc", "member": 1, "action":600}}
{ "votes": { "timestamp": 1557475705, "password": "abc", "member": 1}}
{ "trolls": { "timestamp": 1557477055 }}

