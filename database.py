import sqlite3


DATABASE_FILE = "Database.db"
last_logged_in_user_id = None

def create_table():
    """Create the tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            user_id INTEGER PRIMARY KEY,
            password TEXT NOT NULL,
            age INTEGER CHECK(age >= 0 AND age <= 120),
            sex INTEGER CHECK(sex IN (0, 1))   
        )
    ''')
    conn.commit()
    conn.close()

def insert_user_data(user_id, password, age, sex):
    existing_user = fetch_user_data(user_id,password)
    if existing_user:
        return False  
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_info (user_id, password, age, sex) VALUES (?, ?, ?, ?)", (user_id, password, age, sex))
    conn.commit()
    return True  

def fetch_user_data(user_id, password):
    """Fetch user data for login and update the last logged-in user."""
    global last_logged_in_user_id  # To update the global variable
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM user_info WHERE user_id = ? AND password = ?
    ''', (user_id, password))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        last_logged_in_user_id = user_id  # Update last logged-in user
    return row

def update_user_data(user_id, user_data):
    """Update user data."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE user_info 
        SET age = ?, sex = ?
        WHERE user_id = ?
    ''', (*user_data, user_id))
    conn.commit()
    conn.close()

def get_user_sex(user_id):
    user_id=1
    """Return the sex of the user given their user_id."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sex FROM user_info WHERE user_id = ?
    ''', (1,))
    row = cursor.fetchone()
    print(row)
    conn.close()
    return row[0] if row else None  # Return sex if found, else None

def get_user_age(user_id):
    """Return the age of the user given their user_id."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT age FROM user_info WHERE user_id = ?
    ''', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    return row[0] if row else None 