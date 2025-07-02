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
    preferences TEXT,
    likes TEXT,
    dislikes TEXT
    
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

def update_user_likes(likes,user_id):
    cursor.execute("""  SELECT likes
                        FROM user_data
                        WHERE user_id = %s""", (user_id))
    lik = cursor.fetchone()
    likes = lik + tuple(likes)
    cursor.execute('''
    UPDATE user_data SET likes = %s WHERE user_id = %s
    ''',(likes,user_id))
    conn.commit()

def update_user_dislikes(dislikes,user_id):
    cursor.execute("""  SELECT dislikes FROM user_data WHERE user_id =%s""",(user_id))
    dis = cursor.fetchone()
    dislikes = dis + tuple(dislikes)
    cursor.execute('''
    UPDATE user_data SET dislikes = %s WHERE user_id = %s
    ''',(dislikes,user_id))
    conn.commit()


def get_news(page_number):
        limit = 50
        offset = (page_number - 1) * limit

        query = """
                SELECT id, headline, points, type,image_url,source_url,created_at
                FROM newsdata
                ORDER BY created_at DESC
                    LIMIT %s \
                OFFSET %s \
                """
        cursor.execute(query, (limit, offset))
        rows = cursor.fetchall()
        return rows

def latest_news_id():
    query = """
            SELECT id
            FROM newsdata
            ORDER BY created_at DESC
            LIMIT 1
            """
    cursor.execute(query)
    latest_id = cursor.fetchone()
    cursor.close()
    return latest_id

def get_user_preference(user_id):
    query = '''
    SELECT preferences , likes , dislikes FROM user_data WHERE user_id = %s
    '''
    cursor.execute(query,user_id)
    prefer = cursor.fetchone()
    return prefer


