import json
import datetime
import array

def leader(timestamp, password, member, connection):

    sql = "INSERT INTO member(login,password,lastUpdate,leader) VALUES ({}, '{}', '{}', {})"
    cursor = connection.cursor()
    cursor.execute(sql.format(member, password, datetime.datetime.fromtimestamp(timestamp), True))
    if(cursor.rowcount<1):
        connection.rollback()
        return(json.dumps({"status": "ERROR"})) 
    connection.commit()
    return(json.dumps({"status": "OK"}))


def protest(timestamp, password, member, action, project, authority,connection):

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
    sql = '''select action.id,action.type, projectid, project.authority,count(nullif(vote.type,'downvote')), count(nullif(vote.type,'upvote'))
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
    sql ='''select member.login, count(nullif(vote.type,'downvote')), count(nullif(vote.type,'upvote')) 
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

def trolls(timestamp, connection):
    cursor = connection.cursor()
    sql ='''select login, upvotes, downvotes, check_active(login,{}) from trolls_view where downvotes>upvotes order by (downvotes-upvotes), login '''
    cursor.execute(sql.format(timestamp))
    rows = []
    row = cursor.fetchone()
    while row is not None:
        rows.append(row)
        row = cursor.fetchone()
    connection.commit()
    return(json.dumps({"status":"OK","data": rows}))
    
