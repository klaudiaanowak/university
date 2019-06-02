
import psycopg2

def run_sql_file(filename, connection):
    '''
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection  
    '''
    
    file = open(filename, 'r')
    sql = " ".join(file.readlines())
    cursor = connection.cursor()
    cursor.execute(sql)    
    connection.commit()
    
    print ("Time elapsed to run the query:")

conn = psycopg2.connect(database = "student", user = "postgres")
print ("Opened database successfully")

# cur = conn.cursor()
# cur.execute("""
#         CREATE TABLE vendors (
#             vendor_id SERIAL PRIMARY KEY,
#             vendor_name VARCHAR(255) NOT NULL
#         )
#         """)
run_sql_file("database.sql", conn)    

print ("Table created successfully")

conn.commit()
conn.close()