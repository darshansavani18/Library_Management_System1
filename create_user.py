import tkinter as tk
from tkinter import messagebox
import sqlite3

def open_create_user(root):
    win = tk.Toplevel(root)
    win.title("Create New User")
    win.state("zoomed")
    win.configure(bg="#f2f4f8")
    win.resizable(False, False)

    # ----- CARD -----
    card = tk.Frame(win, bg="white", width=400, height=360)
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    tk.Label(
        card,
        text="Create New User",
        font=("Segoe UI", 18, "bold"),
        fg="#1e3c72",
        bg="white"
    ).pack(pady=20)

    # Username
    tk.Label(card, text="Username", bg="white").pack(anchor="w", padx=40)
    new_user = tk.Entry(card, bg="#f0f0f0", bd=0, font=("Segoe UI", 12))
    new_user.pack(fill="x", padx=40, pady=5, ipady=8)

    # Password
    tk.Label(card, text="Password", bg="white").pack(anchor="w", padx=40)
    new_pass = tk.Entry(card, bg="#f0f0f0", bd=0, show="•", font=("Segoe UI", 12))
    new_pass.pack(fill="x", padx=40, pady=5, ipady=8)

    # Role
    tk.Label(card, text="Role (admin / user)", bg="white").pack(anchor="w", padx=40)
    new_role = tk.Entry(card, bg="#f0f0f0", bd=0, font=("Segoe UI", 12))
    new_role.pack(fill="x", padx=40, pady=5, ipady=8)

    # ---------- SAVE USER ----------
    def save_user():
        username = new_user.get().strip()
        password = new_pass.get().strip()
        role = new_role.get().strip().lower()

        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required")
            return

        if role not in ("admin", "user"):
            messagebox.showerror("Error", "Role must be admin or user")
            return

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

        try:
            cur.execute(
                "INSERT INTO login2(username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            conn.commit()
            messagebox.showinfo("Success", "User created successfully")
            win.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

        finally:
            conn.close()

    # Button
    tk.Button(
        card,
        text="CREATE USER/Admin",
        bg="#1e3c72",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        bd=0,
        cursor="hand2",
        command=save_user
    ).pack(pady=25, ipadx=20, ipady=8)

    tk.Button(
        win,
        text="Close",
        bg="red",
        fg="white",
        width=10,
        command=win.destroy
    ).pack(pady=10)
