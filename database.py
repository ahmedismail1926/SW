import sqlite3

DATABASE_FILE = "Database.db"

def create_table():
    """Create the tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
           user_id INTEGER PRIMARY KEY,
            age INTEGER CHECK(age >= 0 AND age <= 120),
            sex INTEGER CHECK(sex IN (0, 1)),
            cp INTEGER CHECK(cp IN (0, 1, 2, 3)),
            trestbps BLOB CHECK(trestbps > 0),
            chol INTEGER CHECK(chol > 0),
            fbs NUMERIC CHECK(fbs IN (0, 1)),
            restecg INTEGER CHECK(restecg IN (0, 1, 2)),
            thalach INTEGER CHECK(thalach > 0),
            exang INTEGER CHECK(exang IN (0, 1)),
            oldpeak REAL CHECK(oldpeak >= 0),
            password INTEGER,
            PRIMARY KEY(user_id, password)
        )
    ''')
    conn.commit()
    conn.close()

def insert_credentials(user_id, password):
    """Insert new credentials into the database during sign-up."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO user_info (user_id, password)
            VALUES (?, ?)
        ''', (user_id, password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("User ID already exists.")
    finally:
        conn.close()

def insert_user_data(user_id, password):
    """Alias for inserting user credentials."""
    insert_credentials(user_id, password)

def fetch_user_data(user_id, password):
    """Fetch user data for login."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM user_info WHERE user_id = ? AND password = ?
    ''', (user_id, password))
    row = cursor.fetchone()
    conn.close()
    return row

def update_user_data(user_id, user_data):
    """Update user data."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE user_info 
        SET age = ?, sex = ?, cp = ?, trestbps = ?, chol = ?, fbs = ?, restecg = ?, thalach = ?, exang = ?, oldpeak = ?
        WHERE user_id = ?
    ''', (*user_data, user_id))
    conn.commit()
    conn.close()
