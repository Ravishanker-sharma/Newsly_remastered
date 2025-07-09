import psycopg2
from datetime import datetime
import uuid
import bcrypt
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
    section TEXT,
    image_url TEXT,
    source_url TEXT,
    created_at TIMESTAMP,
    type TEXT,
    faq TEXT
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
    password TEXT
    )
    ''')

def update_news_data():
    try :
        with open('/Users/ravisharma/PycharmProjects/Newsly_remastered/Database/temp.txt', 'r', encoding='utf-8') as f:
            data = f.read()
        data = eval(data)
        print(len(data))
        for i in data:
            points = '.'.join(i["Paragraphs"])
            faqs = '||'.join(i["faq"])
            i['faq'] = faqs
            i['Paragraphs'] = points
            i["created_at"] = datetime.now().isoformat()
            cursor.execute(
                '''INSERT INTO newsdata (headline,points,section,image_url,source_url,created_at,type,faq) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
                (i['headline'], i['Paragraphs'], i['section'], i['image_url'], i['source'], i['created_at'],i["type"],i["faq"]))
        conn.commit()
        print("News data Updated!")
    except Exception as e:
        print(e)

def signup(user):
    print(user)
    password_hash = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
    password = password_hash.decode('utf-8')
    try:
        # Step 1: Check if email exists
        cursor.execute("SELECT * FROM user_data WHERE email = %s LIMIT 1", (user['email'],))
        result = cursor.fetchone()

        if result:
            print("User exists:", result)
            return result  # Return existing user

        # Step 2: Insert new user if not found
        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO user_data (name, age, user_id, email,password) VALUES (%s, %s, %s, %s,%s)",
            (user['name'], user['age'], user_id, user['email'],password)
        )
        conn.commit()
        print("User Added!")
        return user_id

    except Exception as e:
        print("Database error:", e)
        return None

def login(user):
    try:
        cursor.execute("SELECT password,user_id FROM user_data WHERE email = %s", (user['email'],))
        result = cursor.fetchone()
        password = result[0].encode('utf-8')
        if bcrypt.checkpw(user['password'].encode('utf-8'),password):
            return result[1]
        else:
            return False
    except Exception as e:
        print("Database error:", e)

def check_user(user):
    try:
        cursor.execute("SELECT * FROM user_data WHERE email = %s", (user["email"],))
        result = cursor.fetchone()
        if result:
            return 1  # User exists
        else:
            return 0  # No user found
    except Exception as e:
        print("Database error:", e)
        return 0


def get_news(page_number,section=None,limit=20):
        offset = (page_number - 1) * limit
        if section != None:
            query = """
                    SELECT id, headline, points, section, image_url, source_url, type, faq
                    FROM newsdata \
                    WHERE section = %s
                    ORDER BY created_at DESC
                        LIMIT %s \
                    OFFSET %s \
 \
                    """
            cursor.execute(query, (section, limit, offset))
            rows = cursor.fetchall()
            return rows
        else:
            query = """
                    SELECT id, headline, points, section, image_url, source_url, type, faq
                    FROM newsdata \
                    ORDER BY created_at DESC
                        LIMIT %s \
                    OFFSET %s \
 \
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
    SELECT  likes , dislikes FROM user_data WHERE user_id = %s
    '''
    cursor.execute(query,(user_id,))
    prefer = cursor.fetchone()
    return prefer

def fetch_news_via_id(news_id):
    query = '''SELECT headline, points, section,faq,image_url  FROM newsdata WHERE id = %s'''
    cursor.execute(query, (news_id,))
    prefer = cursor.fetchone()
    return prefer

def Format_news(page_number,section,limit=20):
    news = get_news(page_number,section,limit)
    output = []
    for i in news:
        info = dict()
        info["id"] = i[0]
        info["headline"] = i[1]
        info["bulletPoints"] = i[2].split("..")
        if i[4] == None or i[4] == "No_image" or i[4] == "":
            info["imageUrl"] = r"https://res.cloudinary.com/dxysb8v1a/image/upload/fl_preserve_transparency/v1751529660/newslylogo_eyrc2v.jpg"
        else:
            info["imageUrl"] = i[4]
        info["sourceIconUrl"] = i[5]
        info["source"] = "Hindustan Times"
        info["section"] = i[3].lower()
        info["type"] = i[6].capitalize()
        output.append(info)
    return output


if __name__ == '__main__':
    # update_news_data()
    # data = get_news(1,"World")[1]
    data = list(fetch_news_via_id(85))
    print(data)

