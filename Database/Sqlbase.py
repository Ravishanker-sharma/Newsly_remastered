import psycopg2
from datetime import datetime
import uuid
conn = psycopg2.connect(
    dbname = 'newsly_base',
    password = '1234',
    user = 'postgres',
    host = 'localhost',
    port = '5432'
)
cursor = conn.cursor()

print('Connected to the database!')

def check_table_existence(table_name):
    cursor.execute(
        '''
        SELECT EXISTS(
        SELECT FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name = %s
        )
        ''',(table_name,)
    )
    exist = cursor.fetchone()[0]
    return exist

if check_table_existence('newsdata') == False:
    cursor.execute( """
    CREATE TABLE newsdata (
    id SERIAL PRIMARY KEY,
    headline TEXT,
    points TEXT,
    type TEXT,
    image_url TEXT,
    source_url TEXT,
    created_at TIMESTAMP
    )
    """)
    print('Created Table : newsdata')

if check_table_existence('user_data') == False:
    cursor.execute('''
    CREATE TABLE user_data (
    id SERIAL PRIMARY KEY,
    name TEXT,
    age INT,
    user_id TEXT,
    email TEXT UNIQUE NOT NULL,
    preferences TEXT
        )
    ''')

def update_news_data():
    try :
        with open('temp.txt', 'r', encoding='utf-8') as f:
            data = f.read()
        data = eval(data)
        print(len(data))
        for i in data:
            points = '.'.join(i["Paragraphs"])
            i['Paragraphs'] = points
            i["created_at"] = datetime.now().isoformat()
            cursor.execute(
                '''INSERT INTO newsdata (headline,points,type,image_url,source_url,created_at) VALUES (%s,%s,%s,%s,%s,%s)''',
                (i['headline'], i['Paragraphs'], i['type'], i['image_url'], i['source'], i['created_at']))
        conn.commit()
        print("News data Updated!")
    except Exception as e:
        print(e)

def update_user_data(user):
    try:
        cursor.execute(
            '''INSERT INTO user_data (name,age,user_id,email,preferences) VALUES (%s,%s,%s,%s,%s)''',
            (user['name'],user['age'],str(uuid.uuid4()),user['email'],None)
        )
        conn.commit()
        print("User Added!")
    except Exception as e:
        print(e)

def update_user_preference(preference,user_id):
    cursor.execute('''
    UPDATE user_data SET preferences = %s WHERE user_id = %s
    ''',(preference,user_id))
    conn.commit()