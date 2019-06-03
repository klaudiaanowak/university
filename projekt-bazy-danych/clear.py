import psycopg2
import json

connection = psycopg2.connect(database="student", user="init", password="qwerty")
cursor = connection.cursor()
cursor.execute('''DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
    REVOKE ALL PRIVILEGES ON all tables in schema public FROM app;
    DROP USER app;
END $$;''')
connection.commit()
connection.close()
