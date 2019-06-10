import json
import datetime
import array

def leader(timestamp, password, member, connection):

    sql = "INSERT INTO member(login,password,lastUpdate,leader) VALUES ({}, '{}', '{}', {})"
    cursor = connection.cursor()
    cursor.execute(sql.format(member, password, datetime.datetime.fromtimestamp(timestamp), True))
    connection.commit()
    return(json.dumps({"status": "OK"}))


def protest(timestamp, password, member, action, project, authority,connection):
    # sprawdza poprawność hasła
    #sprawdza czy aktywny
    # dodaje członka jeśli nie istnieje
    # dodaje projekt / authority jeśli nie istnieje
    # trigger after insert do aktualizacji last update member

    check_member = "SELECT add_member_if_not_exists({},'{}',{})"
    check_pass = "SELECT check_pass({},'{}','{}')"
    check_active = "SELECT check_active({},{})"
    check_project = "SELECT add_project_if_not_exists({}, {}, {}, {})"
    sql = "INSERT INTO action(id, type, creationDate, author, projectID) VALUES ({}, '{}', '{}', {}, {})"
    cursor = connection.cursor()
    cursor.execute(check_member.format(member,password,timestamp))
    cursor.execute(check_pass.format(member,password,'{True,False}'))
    if(cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    cursor.execute(check_active.format(member,timestamp))
    if (cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    if (authority!= ""):
        cursor.execute(check_project.format(project,member,timestamp,authority))
    cursor.execute(sql.format(action, 'protest', datetime.datetime.fromtimestamp(timestamp), member, project))
    if(cursor.rowcount<1):
        connection.rollback()
        return(json.dumps({"status": "ERROR"})) 
    connection.commit()
    return(json.dumps({"status": "OK"}))

    
def support(timestamp, password, member, action, project, authority,connection):
    # sprawdza poprawność hasła
    # dodaje członka jeśli nie istnieje
    # dodaje projekt / authority jeśli nie istnieje
    # trigger after insert do aktualizacji last update member

    check_member = "SELECT add_member_if_not_exists({},'{}',{})"
    check_pass = "SELECT check_pass({},'{}','{}')"
    check_active = "SELECT check_active({}, {})"
    check_project = "SELECT add_project_if_not_exists({}, {}, {}, {})"
    sql = "INSERT INTO action(id, type, creationDate, author, projectID) VALUES ({}, '{}', '{}', {}, {})"
    cursor = connection.cursor()
    cursor.execute(check_member.format(member,password,timestamp))
    cursor.execute(check_pass.format(member,password,'{True,False}'))
    if(cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    cursor.execute(check_active.format(member,timestamp))
    if (cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"}))  
    if (authority!= ""):
        cursor.execute(check_project.format(project,member,timestamp,authority))
    cursor.execute(sql.format(action, 'support', datetime.datetime.fromtimestamp(timestamp), member, project))
    if(cursor.rowcount<1):
        connection.rollback()
        return(json.dumps({"status": "ERROR"})) 
    connection.commit()
    return(json.dumps({"status": "OK"}))



def upvote(timestamp, password, member, action, connection):

    check_member = "SELECT add_member_if_not_exists({},'{}',{})"
    check_pass = "SELECT check_pass({},'{}','{}')"
    check_active = "SELECT check_active({}, {})"        
    sql = "INSERT INTO vote(member, action, type, timestamp) VALUES ({}, {}, '{}', '{}')"
    cursor = connection.cursor()
    cursor.execute(check_member.format(member,password,timestamp))
    cursor.execute(check_pass.format(member,password,'{True,False}'))
    if(cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    cursor.execute(check_active.format(member,timestamp))
    if (cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"}))  

    cursor.execute(sql.format(member, action, 'upvote', datetime.datetime.fromtimestamp(timestamp)))
    if(cursor.rowcount<1):
        connection.rollback()
        return(json.dumps({"status": "ERROR"})) 
    connection.commit()
    return(json.dumps({"status": "OK"}))

    
def downvote(timestamp, password, member, action, connection):

    check_member = "SELECT add_member_if_not_exists({},'{}',{})"
    check_pass = "SELECT check_pass({},'{}','{}')"
    check_active = "SELECT check_active({}, {})"        
    sql = "INSERT INTO vote(member, action, type, timestamp) VALUES ({}, {}, '{}', '{}')"
    cursor = connection.cursor()
    cursor.execute(check_member.format(member,password,timestamp))
    cursor.execute(check_pass.format(member,password,'{True,False}'))
    if(cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    cursor.execute(check_active.format(member,timestamp))
    if (cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"}))  
    cursor.execute(sql.format(member, action, 'downvote', datetime.datetime.fromtimestamp(timestamp)))
    if(cursor.rowcount<1):
        connection.rollback()
        return(json.dumps({"status": "ERROR"})) 
    connection.commit()
    return(json.dumps({"status": "OK"}))
   
def actions(timestamp, password, member, type, project, authority, connection):
    # sprawdz czy lider, czy poprawne hasło

    check_pass = "SELECT check_pass({},'{}','{}')"
    check_active = "SELECT check_active({}, {})" 
    if(project == "" and authority =="" and type == ""):
        where = ""
    else:
        where = "where "
        condition=[]
        if(type!=""):
            condition.append("action.type = '" + type+ "'")
        if(project!=""):
            condition.append("project.id = " +str(project))
        if(authority!=""):
            condition.append("project.authority = " +str(authority))   
        where = where + ' AND '.join(condition)
    sql = '''select action.id,action.type, projectid, project.authority,count(nullif(vote.type,'upvote')), count(nullif(vote.type,'downvote'))
    from action join project on (project.id = action.projectid) left join vote on (vote.action = action.id) ''' + where + ''' group by action.id, action.type, projectid, project.authority
    order by action.id'''
    cursor = connection.cursor()
    cursor.execute(check_pass.format(member,password,'{True}'))
    if(cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    cursor.execute(check_active.format(member,timestamp))
    if (cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    cursor.execute(sql)
    rows = []
    row = cursor.fetchone()
    while row is not None:
        rows.append(row)
        row = cursor.fetchone()
    update_sql = "UPDATE member SET lastUpdate = to_timestamp(" + str(timestamp) + ") WHERE member.login = " + str(member)
    cursor.execute(update_sql)
    connection.commit()

    return(json.dumps({"status":"OK","data": rows}))

        
def projects(timestamp, member, password,authority,connection):

    check_pass = "SELECT check_pass({},'{}','{}')"
    check_active = "SELECT check_active({}, {})" 
    cursor = connection.cursor()
    cursor.execute(check_pass.format(member,password,'{True}'))
    if(cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    cursor.execute(check_active.format(member,timestamp))
    if (cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    if(authority ==""):
            where = ""
    else:
        where = "where project.authority = " + str(authority);
    sql = '''select id, authority from project ''' + where + " order by id"
    cursor.execute(sql)
    rows = []
    row = cursor.fetchone()
    while row is not None:
        rows.append(row)
        row = cursor.fetchone()
    update_sql = "UPDATE member SET lastUpdate = to_timestamp(" + str(timestamp) + ") WHERE member.login = " + str(member) 
    cursor.execute(update_sql)
    connection.commit()
    return(json.dumps({"status":"OK","data": rows}))

    
def votes(timestamp, member, password, action, project, connection):

    check_pass = "SELECT check_pass({},'{}','{}')"
    check_active = "SELECT check_active({}, {})" 
    cursor = connection.cursor()
    cursor.execute(check_pass.format(member,password,'{True}'))
    if(cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    cursor.execute(check_active.format(member,timestamp))
    if (cursor.fetchone()[0] == False):
        return(json.dumps({"status": "ERROR"})) 
    if(project == "" and action ==""):
        where = ""
    else:
        where = "where "
        condition=[]
        if(project!=""):
            condition.append("action.projectid = " +str(project))
        if(action!=""):
            condition.append("vote.action = " +str(action))   
        where = where + ' AND '.join(condition)
    sql ='''select member.login, count(nullif(vote.type,'upvote')), count(nullif(vote.type,'downvote')) 
    from vote right join member on (member.login = vote.member) left join action on (action.id = vote.action) 
    ''' + where + ''' group by member.login order by member.login'''
    cursor.execute(sql)
    rows = []
    row = cursor.fetchone()
    while row is not None:
        rows.append(row)
        row = cursor.fetchone()
    update_sql = "UPDATE member SET lastUpdate = to_timestamp(" + str(timestamp) + ") WHERE member.login = " + str(member)
    cursor.execute(update_sql)
    connection.commit()
    return(json.dumps({"status":"OK","data": rows}))
 
    
    
    
{ "open": { "database": "student", "login": "init", "password": "qwerty"}}
{ "leader": { "timestamp": 1557473000, "password": "abc", "member": 1}}
{ "leader": { "timestamp": 1557474000, "password": "asd", "member": 2}}
{ "leader": { "timestamp": 1557474000, "password": "asd", "member": 3}}

{ "open": { "database": "student", "login": "app", "password": "qwerty"}}
{ "upvote": { "timestamp": 1557476000, "password": "asd", "member": 2, "action":310}}
{"votes": {"timestamp": 1557477704, "member": 2, "password": "asd"}}  
{"votes": {"timestamp": 1557477704, "member": 2, "password": "asd", "project": 8000}}   
{"votes": {"timestamp": 1557477704, "member": 2, "password": "asd", "project": 8000, "action": 310}}                                   
{"projects": {"timestamp": 1557477704, "member": 2, "password": "asd"}}
{"projects": {"timestamp": 1557477704, "member": 2, "password": "asd","authority": 10000}}
{ "actions": { "timestamp": 1557475704, "member": 5, "password": "abc"}}
{ "actions": { "timestamp": 1557475704, "member": 1, "password": "abc", "project": 8000}}
{ "actions": { "timestamp": 1557475704, "member": 1, "password": "abc", "type": "protest"}}
{ "actions": { "timestamp": 1557405704, "member": 1, "password": "abc", "project": 5000, "authority":10000}}
{ "protest": { "timestamp": 1557475723, "password": "123", "member": 1, "action":110, "project":7000, "authority":20000}}
{ "protest": { "timestamp": 57475723, "password": "1123", "member": 40, "action":99, "project":7000, "authority":10000}}
{ "support": { "timestamp": 1557475701, "password": "123", "member": 5, "action":1000, "project":5000, "authority":10000}}
{ "support": { "timestamp": 1557475701, "password": "1123", "member": 7, "action":310, "project":8000}}
{ "support": { "timestamp": 1557475701, "password": "1123", "member": 7, "action":310, "project":8000, "authority":20000}}
{ "support": { "timestamp": 1557475701, "password": "1123", "member": 7, "action":320, "project":8000}}
{ "upvote": { "timestamp": 1557475702, "password": "asd", "member": 2, "action":1000}}
{ "upvote": { "timestamp": 1557475702, "password": "asd", "member": 2, "action":310}}
{ "upvote": { "timestamp": 1557476000, "password": "asd", "member": 2, "action":310}}
{ "downvote": { "timestamp": 1557475703, "password": "abc", "member": 1, "action":1000}}
{ "downvote": { "timestamp": 1557475704, "password": "abc", "member": 1, "action":310}}
{ "actions": { "timestamp": 1557475904, "member": 1, "password": "abc"}}
{ "votes": { "timestamp": 1557575705, "password": "abc", "member": 1}}
{ "trolls": { "timestamp": 1557477055 }}

