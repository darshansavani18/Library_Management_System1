from tkinter import ttk
import sqlite3
from tkinter import messagebox
import tkinter as tk

def open_receive_books_list(root):
    win = tk.Toplevel(root)
    win.title("Receive Books List")
    win.state("zoomed")
    win.configure(bg="#f2f4f8")

    # ================= HEADER =================
    header = tk.Frame(win, bg="white", height=80)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Receive Books Report",
        font=("Segoe UI", 20, "bold"),
        fg="#1e3c72",
        bg="white"
    ).pack(side="left", padx=20)

    tk.Label(header, text="From:", bg="white").pack(side="left", padx=(40,5))
    from_date = tk.Entry(header)
    from_date.pack(side="left")

    tk.Label(header, text="To:", bg="white").pack(side="left", padx=(10,5))
    to_date = tk.Entry(header)
    to_date.pack(side="left")

    # ================= TABLE =================
    table_frame = tk.Frame(win, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
    y_scroll = tk.Scrollbar(table_frame, orient="vertical")

    columns = (
        "date","srno","card","acc","name","rno",
        "title","author","subject","publisher"
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
        "Issue Date","Sr No","Card No","Acc No","Name","Roll No",
        "Title","Author","Subject","Publisher"
    ]

    for col, head in zip(columns, headings):
        table.heading(col, text=head)
        table.column(col, width=150, anchor="center")

    table.column("title", width=250, anchor="w")

    # ================= LOAD DATA =================
    def load_data(query=None, params=()):
        table.delete(*table.get_children())

        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()

        if query:
            cur.execute(query, params)
        else:
            cur.execute("""
                SELECT 
                    i.issue_date,
                    i.id,
                    i.card_no,
                    i.acc_no,
                    m.member_name,
                    m.rno,
                    b.title,
                    b.author,
                    b.sub,
                    b.publisher
                FROM issue_books i
                JOIN members m ON i.card_no = m.card_no
                JOIN books b ON i.acc_no = b.acc_no
            """)

        rows = cur.fetchall()
        conn.close()

        for row in rows:
            table.insert("", "end", values=row)

    load_data()

    # ================= FILTER BY DATE =================
    def filter_data():
        f = from_date.get()
        t = to_date.get()

        if f == "" or t == "":
            messagebox.showwarning("Error", "Enter both dates")
            return

        load_data("""
            SELECT 
                i.issue_date,
                i.id,
                i.card_no,
                i.acc_no,
                m.member_name,
                m.rno,
                b.title,
                b.author,
                b.sub,
                b.publisher
            FROM issue_books i
            JOIN members m ON i.card_no = m.card_no
            JOIN books b ON i.acc_no = b.acc_no
            WHERE i.issue_date BETWEEN ? AND ?
        """, (f, t))

    tk.Button(
        header,
        text="Search",
        bg="#1e3c72",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        command=filter_data
    ).pack(side="left", padx=20)
