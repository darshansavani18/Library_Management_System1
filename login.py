import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui.dashboard import open_dashboard

# ---------- DATABASE ----------
conn = sqlite3.connect("LMS.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS login2(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT    
    )
""")
cur.execute("""
    INSERT OR IGNORE INTO login2(username,password,role)
    VALUES('admin','admin123','admin')
""")
conn.commit()
conn.close()

# ---------- ROOT ----------
root = tk.Tk()
root.title("Library Management System")
root.state("zoomed")
root.configure(bg="#f2f4f8")

screen_W = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

def on_login_show():
    user_var.delete(0, tk.END)
    pass_var.delete(0, tk.END)
    role_var.delete(0, tk.END)
    user_var.focus_set()

# ---------- LOGIN ACTION (SECURE) ----------
def login_action():
    username = user_var.get()
    password = pass_var.get()

    conn = sqlite3.connect("LMS.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT role FROM login2
        WHERE username=? AND password=?
    """, (username, password))

    result = cur.fetchone()
    conn.close()

    if result:
        db_role = result[0]   # 🔥 ROLE COMES FROM DATABASE ONLY

        root.withdraw()
        open_dashboard(root, on_login_show, db_role)

    else:
        messagebox.showerror("Error", "Invalid username or password")

# ---------- LEFT PANEL ----------
left_panel = tk.Frame(
    root,
    bg="#1e3c72",
    width=int(screen_W * 0.45),
    height=screen_h
)
left_panel.place(x=0, y=0)

tk.Label(
    left_panel,
    text="Library\nManagement\nSystem",
    font=("Segoe UI", 36, "bold"),
    fg="white",
    bg="#1e3c72",
    justify="left"
).place(x=80, y=175)

tk.Label(
    left_panel,
    text="Secure • Fast • User Friendly",
    font=("Segoe UI", 14),
    fg="#cfd9ff",
    bg="#1e3c72"
).place(x=80, y=370)

# ---------- LOGIN CARD ----------
login_card = tk.Frame(root, bg="white", width=450, height=450)
login_card.place(relx=0.65, rely=0.5, anchor="center")

tk.Label(
    login_card,
    text="LOGIN",
    font=("Segoe UI", 24, "bold"),
    fg="#1e3c72",
    bg="white"
).place(x=160, y=40)

tk.Label(login_card, text="Username", bg="white").place(x=60, y=120)
user_var = tk.Entry(login_card, bg="#f0f0f0", bd=0, font=("Segoe UI", 12))
user_var.place(x=60, y=145, width=300, height=40)

tk.Label(login_card, text="Password", bg="white").place(x=60, y=200)
pass_var = tk.Entry(
    login_card,
    bg="#f0f0f0",
    bd=0,
    show="•",
    font=("Segoe UI", 12)
)
pass_var.place(x=60, y=225, width=300, height=40)

tk.Label(login_card, text="", bg="white").place(x=60, y=280)
role_var = tk.Entry(
    login_card,
    bg="#f0f0f0",
    bd=0,
    font=("Segoe UI", 12),
    state="disabled"   # 🔒 ROLE CANNOT BE TYPED
)
#role_var.place(x=60, y=305, width=300, height=40)
tk.Button(
    login_card,
    text="LOGIN",
    bg="#1e3c72",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    bd=0,
    cursor="hand2",
    command=login_action
).place(x=60, y=320, width=300, height=45)

root.mainloop()
