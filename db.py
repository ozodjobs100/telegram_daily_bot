import sqlite3

conn = sqlite3.connect('botdata.db', check_same_thread=False)
cursor = conn.cursor()

def setup():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()

def add_user(user_id):
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()

def get_users():
    cursor.execute('SELECT user_id FROM users')
    return [row[0] for row in cursor.fetchall()]

def set_message(text):
    cursor.execute('DELETE FROM messages')
    cursor.execute('INSERT INTO messages (text) VALUES (?)', (text,))
    conn.commit()

def get_message():
    cursor.execute('SELECT text FROM messages ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return "Salom! Bu botdan foydalanganingiz uchun rahmat!"
