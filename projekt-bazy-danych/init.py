import psycopg2
import json
from functions import *

def run_sql_file(filename, connection):

    file = open(filename, 'r')
    sql = " ".join(file.readlines())
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    print("Time elapsed to run the query:")


def fun_open(database, user, password):
    try:
        conn = psycopg2.connect(database=database, user=user, password=password)
        print("Opened database successfully")
    except:
        print(json.dumps({"status": "ERROR"}))

    if (user == 'init'):
        try:
            run_sql_file("database.sql", conn)
            print(json.dumps({"status": "OK"}))
            print("Table created successfully")
        except:
            print(json.dumps({"status": "ERROR"}))
        while (True):
            new_input = input()
            json_input = json.loads(new_input)
            if(list(json_input.keys())[0] == 'leader'):
                open_json = json.loads(json.dumps(json_input["leader"]))
                print(leader(open_json["timestamp"], open_json["password"], open_json["member"],conn))
            else:
                print(json.dumps({"status": "ERROR"}))

    elif (user == 'app'):
        while (True):
            new_input = input()
            json_input = json.loads(new_input)
            if(list(json_input.keys())[0] == 'protest'):
                open_json = json.loads(json.dumps(json_input["protest"]))
                if "auhority" in open_json.keys():
                    authority = open_json["authority"]
                else:
                    authority = ""
                print(protest(open_json["timestamp"], open_json["password"], open_json["member"], open_json["action"], open_json["project"], authority, conn))
            if(list(json_input.keys())[0] == 'support'):
                open_json = json.loads(json.dumps(json_input["support"]))
                if "auhority" in open_json.keys():
                    authority = open_json["authority"]
                else:
                    authority = ""
                print(support(open_json["timestamp"], open_json["password"], open_json["member"], open_json["action"], open_json["project"], authority, conn))
            if(list(json_input.keys())[0] == 'upvote'):
                open_json = json.loads(json.dumps(json_input["upvote"]))
                print(upvote(open_json["timestamp"], open_json["password"], open_json["member"], open_json["action"]))
            if(list(json_input.keys())[0] == 'downvote'):
                open_json = json.loads(json.dumps(json_input["downvote"]))
                print(downvote(open_json["timestamp"], open_json["password"], open_json["member"], open_json["action"]))
            if(list(json_input.keys())[0] == 'actions'):
                open_json = json.loads(json.dumps(json_input["actions"]))
                #actions(open_json["database"], open_json["login"], open_json["password"])
            if(list(json_input.keys())[0] == 'projects'):
                open_json = json.loads(json.dumps(json_input["projects"]))
                #projects(open_json["database"], open_json["login"], open_json["password"])
            if(list(json_input.keys())[0] == 'votes'):
                open_json = json.loads(json.dumps(json_input["votes"]))
                #votes(open_json["database"], open_json["login"], open_json["password"])
            if(list(json_input.keys())[0] == 'trolls'):
                open_json = json.loads(json.dumps(json_input["trolls"]))
                #trolls(open_json["database"], open_json["login"], open_json["password"])
            else:
                print(json.dumps({"status": "ERROR"}))
    else:
        print(json.dumps({"status": "ERROR"}))


    conn.commit()
    conn.close()


def main():

    json_input = input()
    #json_input = '{ "open": { "database": "student", "login": "init", "password": "qwerty"}}'
    json_loaded = json.loads(json_input)


    if(list(json_loaded.keys())[0] == 'open'):
        open_json = json.loads(json.dumps(json_loaded["open"]))
        fun_open(open_json["database"], open_json["login"], open_json["password"])
    else :
        print(json.dumps({"status": "ERROR"}))
    # conn = psycopg2.connect(database = "student", user = "postgres")


if __name__ == "__main__":
    main()
