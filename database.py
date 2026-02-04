import sqlite3

db_name = "LMS.db"

def get_connection():
    return sqlite3.connect(db_name)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        acc_no INTEGER,
        bar_code INTEGER,
        title TEXT,
        author TEXT,
        publisher TEXT,
        topic TEXT,
        sub TEXT,
        edition TEXT,
        year TEXT,
        no_page INTEGER,
        volume INTEGER,
        source TEXT,
        bill_no INTEGER,
        bill_date TEXT,
        e_cost INTEGER,
        class TEXT,
        b_no INTEGER,
        isbn TEXT,
        location TEXT,
        remarks TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS members(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT,
        card_no TEXT,
        rno TEXT,
        member_name TEXT,
        father_name TEXT,
        address TEXT,
        city TEXT,
        district TEXT,
        department TEXT,
        contact1 TEXT,
        contact2 TEXT,
        sitting_plan TEXT,
        remarks TEXT,
        valid_date TEXT
    )
    """)

    cur.execute("PRAGMA table_info(books)")
    columns = [col[1] for col in cur.fetchall()]

    if "is_issued" not in columns:
        cur.execute("ALTER TABLE books ADD COLUMN is_issued INTEGER DEFAULT 0")

    if "issued_to_card" not in columns:
        cur.execute("ALTER TABLE books ADD COLUMN issued_to_card TEXT")

    if "issue_date" not in columns:
        cur.execute("ALTER TABLE books ADD COLUMN issue_date TEXT")

    if "issue_remarks" not in columns:
        cur.execute("ALTER TABLE books ADD COLUMN issue_remarks TEXT")

    cur.execute(
    """CREATE TABLE IF NOT EXISTS issue_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_date TEXT,
        card_no TEXT,
        acc_no INTEGER)"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT UNIQUE,
    description TEXT)"""
    )

    conn.commit()
    conn.close()