import sqlite3
conn = sqlite3.connect('database/attendance.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roll_no TEXT UNIQUE,
    department TEXT,
    mobile TEXT,
    password TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT,
    date TEXT,
    status TEXT
)""")

cur.execute("INSERT OR IGNORE INTO admin (email, password) VALUES ('admin@gmail.com', 'admin123')")
cur.execute("INSERT OR IGNORE INTO students (name, roll_no, department, mobile, password) VALUES ('Ashok', '713523AM009', 'AIMK', '7904271813', 'ashok123')")
conn.commit()
conn.close()
print("✅ Database initialized successfully!")
