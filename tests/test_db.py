from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

try:
	with psycopg2.connect(host=host,port=port,user=user,password=password,database=db_name) as conn:
		print(f"Connected to db with host name: {host}")
		with conn.cursor() as cursor:
			data_insert = '''INSERT INTO business	(name,website,status_code,safety,latency,phone)
				  VALUES (%s,%s,%s,%s,%s,%s)
			  	ON CONFLICT(website)
			  	DO UPDATE SET
			  		status_code = EXCLUDED.status_code,
					latency = EXCLUDED.latency;
			'''
			info = ("Test", "test@test.com", "200", "TRUE", "0.34", "999222333")
			cursor.execute(data_insert, info)			
			conn.commit()

except Exception as e:
	print(f"Error connecting to the db: {e}")
