import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")


def save_to_db(dic:list):
    """Persist scraped data into PostgreSQL database.

    Inserts new records and updates existing ones on conflict.

    Args:
        dic (list[dict]): List of business data entries.
    """ 
    blacklist = ['tripadvisor', 'thefork', 'zomato', 'yelp', 'pai.pt', 'eatbu', 'wix', 'google']


    try:
        with psycopg2.connect(host=host,port=port,user=user,password=password,database=db_name) as conn:
            print(f"Connected to db with host name: {host}")
            with conn.cursor() as cursor:
                for row in dic:
                    url = row['Url'].lower()
                    if any(bad_word in url for bad_word in blacklist):
                        continue

                    data_insert = '''INSERT INTO business	(name,email,url,phone,security,status,latency,industry,category)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT(name, email)
                        DO UPDATE SET
                            status = EXCLUDED.status,
                            latency = EXCLUDED.latency,
                            industry = EXCLUDED.industry,
                            category = EXCLUDED.category;
                    '''
                    info = (row['Name'], row['Email'], row['Url'], row['Phone'], row['Security'], row['Status'], row['Latency'], row['Industry'],row['Category'])
                    cursor.execute(data_insert, info)			
            conn.commit()
    except Exception as e:
        print(f"Error connecting to the db or inserting data: {e}")
