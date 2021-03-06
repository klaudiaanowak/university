import psycopg2
import json
import sys
from functions import *

def run_sql_file(filename, connection):

    file = open(filename, 'r')
    sql = " ".join(file.readlines())
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()



def fun_open(database, user, password):
    try:
        conn = psycopg2.connect(database=database, user=user, password=password)
        print(json.dumps({"status": "OK"}))
    except:
        print(json.dumps({"status": "ERROR"}))

    if (user == 'init'):
        run_sql_file("database.sql", conn)

        for new_input in sys.stdin:
            if(new_input == '\n'):
                break
            try:
                json_input = json.loads(new_input)
                if(list(json_input.keys())[0] == 'leader'):
                    open_json = json.loads(json.dumps(json_input["leader"]))
                    print(leader(open_json["timestamp"], open_json["password"], open_json["member"],conn))
                else:
                    print(json.dumps({"status": "ERROR"}))
            except:
                print("init")
                print(json.dumps({"status": "ERROR"}))

    elif (user == 'app'):
        for new_input in sys.stdin:
            if(new_input == '\n'):
                break
            try:
                json_input = json.loads(new_input)
            except:
                print(json.dumps({"status": "ERROR"}))
                continue
            if(list(json_input.keys())[0] == 'protest'):
                open_json = json.loads(json.dumps(json_input["protest"]))
                if "authority" in open_json.keys():
                    authority = open_json["authority"]
                else:
                    authority = ""
                print(protest(open_json["timestamp"], open_json["password"], open_json["member"], open_json["action"], open_json["project"], authority, conn))
            elif(list(json_input.keys())[0] == 'support'):
                open_json = json.loads(json.dumps(json_input["support"]))
                if "authority" in open_json.keys():
                    authority = open_json["authority"]
                else:
                    authority = ""
                print(support(open_json["timestamp"], open_json["password"], open_json["member"], open_json["action"], open_json["project"], authority, conn))
            elif(list(json_input.keys())[0] == 'upvote'):
                open_json = json.loads(json.dumps(json_input["upvote"]))
                print(upvote(open_json["timestamp"], open_json["password"], open_json["member"], open_json["action"], conn))
            elif(list(json_input.keys())[0] == 'downvote'):
                open_json = json.loads(json.dumps(json_input["downvote"]))
                print(downvote(open_json["timestamp"], open_json["password"], open_json["member"], open_json["action"], conn))
            elif(list(json_input.keys())[0] == 'actions'):
                open_json = json.loads(json.dumps(json_input["actions"]))
                if "authority" in open_json.keys():
                    authority = open_json["authority"]
                else:
                    authority = ""
                if "type" in open_json.keys():
                    type = open_json["type"]
                else:
                    type = ""
                if "project" in open_json.keys():
                    project = open_json["project"]
                else:
                    project = ""
                print(actions(open_json["timestamp"], open_json["password"], open_json["member"],type, project, authority, conn))
            elif(list(json_input.keys())[0] == 'projects'):
                open_json = json.loads(json.dumps(json_input["projects"]))
                if "authority" in open_json.keys():
                    authority = open_json["authority"]
                else:
                    authority = ""
                print(projects(open_json["timestamp"], open_json["member"], open_json["password"],authority,conn))
            elif(list(json_input.keys())[0] == 'votes'):
                open_json = json.loads(json.dumps(json_input["votes"]))
                if "action" in open_json.keys():
                    action = open_json["action"]
                else:
                    action = ""
                if "project" in open_json.keys():
                    project = open_json["project"]
                else:
                    project = ""
                print(votes(open_json["timestamp"], open_json["member"], open_json["password"],action, project, conn))
            elif(list(json_input.keys())[0] == 'trolls'):
                open_json = json.loads(json.dumps(json_input["trolls"]))
                print(trolls(open_json["timestamp"],conn))

    else:
        print("user")
        print(json.dumps({"status": "ERROR"}))


    conn.commit()
    conn.close()


def main():

    json_input = input()
    json_loaded = json.loads(json_input)


    if(list(json_loaded.keys())[0] == 'open'):
        open_json = json.loads(json.dumps(json_loaded["open"]))
        fun_open(open_json["database"], open_json["login"], open_json["password"])
    else :
        print("not open")
        print(json.dumps({"status": "ERROR"}))



if __name__ == "__main__":
    main()
