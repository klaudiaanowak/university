import psycopg2
import json


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
        run_sql_file("database.sql", conn)
        print(json.dumps({"status": "OK"}))
        print("Table created successfully")
    except:
        print(json.dumps({"status": "ERROR"}))

    while (True):
        new_input = input()
        json_input = json.loads(input)


    conn.commit()
    conn.close()


def main():

    #json_input = input()
    json_input = '{ "open": { "database": "student", "login": "init", "password": "qwerty"}}'
    json_loaded = json.loads(json_input)


    if(list(json_loaded.keys())[0] == 'open'):
        open_json = json.loads(json.dumps(json_loaded["open"]))
        fun_open(open_json["database"], open_json["login"], open_json["password"])

    # conn = psycopg2.connect(database = "student", user = "postgres")


if __name__ == "__main__":
    main()
