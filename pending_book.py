import tkinter as tk
from tkinter import ttk
import sqlite3

def open_pending_books(root):
    win = tk.Toplevel(root)
    win.title("Pending Books")
    win.state("zoomed")
    win.configure(bg="#f2f4f8")

    # ================= HEADER =================
    tk.Label(
        win,
        text="Pending Books Report",
        font=("Segoe UI", 22, "bold"),
        fg="#1e3c72",
        bg="#f2f4f8"
    ).pack(pady=15)

    # ================= TABLE =================
    table_frame = tk.Frame(win, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
    y_scroll = tk.Scrollbar(table_frame, orient="vertical")

    columns = (
        "date", "card", "rno", "name",
        "acc", "title", "author", "subject", "publisher"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        xscrollcommand=x_scroll.set,
        yscrollcommand=y_scroll.set
    )

    x_scroll.config(command=table.xview)
    y_scroll.config(command=table.yview)

    x_scroll.pack(side="bottom", fill="x")
    y_scroll.pack(side="right", fill="y")
    table.pack(fill="both", expand=True)

    headings = [
        "Issue Date", "Card No", "Roll No", "Member Name",
        "Acc No", "Title", "Author", "Subject", "Publisher"
    ]

    for col, head in zip(columns, headings):
        table.heading(col, text=head)
        table.column(col, width=160, anchor="center")

    table.column("title", width=260, anchor="w")
    table.column("name", width=200, anchor="w")

    # ================= LOAD DATA =================
    def load_pending():
        table.delete(*table.get_children())

        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()

        cur.execute("""
            SELECT
                b.issue_date,
                m.card_no,
                m.rno,
                m.member_name,
                b.acc_no,
                b.title,
                b.author,
                b.sub,
                b.publisher
            FROM books b
            JOIN members m ON b.issued_to_card = m.card_no
            WHERE b.is_issued = 1
        """)

        rows = cur.fetchall()
        conn.close()

        for row in rows:
            table.insert("", "end", values=row)

    load_pending()
