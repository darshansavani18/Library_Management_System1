from tkinter import ttk, messagebox
import sqlite3
import datetime
import tkinter as tk

def open_issue_book(root):
    win = tk.Toplevel(root)
    win.title("Issue Book")
    win.state("zoomed")
    win.configure(bg="#f2f4f8")

    # ================= HEADER =================
    header = tk.Frame(win, bg="white", height=80)
    header.pack(fill="x")

    issue_date = tk.StringVar()
    sr_no = tk.StringVar()
    card_no = tk.StringVar()
    acc_no = tk.StringVar()
    header_remark = tk.StringVar()

    def h_field(text, var, col):
        tk.Label(header, text=text, bg="white")\
            .grid(row=0, column=col*2, padx=8, pady=10)
        tk.Entry(header, textvariable=var, width=18)\
            .grid(row=0, column=col*2+1, padx=8)

    h_field("Date of Receipt", issue_date, 0)
    h_field("Sr No", sr_no, 1)
    h_field("Card No", card_no, 2)
    h_field("Accession No", acc_no, 3)
    h_field("Remarks", header_remark, 4)

    # ================= BODY =================
    body = tk.Frame(win, bg="#f2f4f8")
    body.pack(fill="both", expand=True, padx=10, pady=10)

    # ================= LEFT: STUDENT =================
    left = tk.Frame(body, bg="white", width=350)
    left.pack(side="left", fill="y", padx=5)
    left.pack_propagate(False)

    tk.Label(left, text="Student Details",
             font=("Segoe UI", 14, "bold"), bg="white").pack(pady=8)

    s = {}
    def s_field(lbl, key):
        tk.Label(left, text=lbl, bg="white").pack(anchor="w", padx=15)
        e = tk.Entry(left)
        e.pack(fill="x", padx=15, pady=4)
        s[key] = e

    s_field("Group", "group")
    s_field("Roll No", "rno")
    s_field("Name", "name")
    s_field("Contact No 1", "c1")
    s_field("Contact No 2", "c2")
    s_field("Remarks", "remarks")

    # ================= MIDDLE: BOOK =================
    middle = tk.Frame(body, bg="white", width=400)
    middle.pack(side="left", fill="y", padx=5)
    middle.pack_propagate(False)

    tk.Label(middle, text="Book Details",
             font=("Segoe UI", 14, "bold"), bg="white").pack(pady=8)

    b = {}
    def b_field(lbl, key):
        tk.Label(middle, text=lbl, bg="white").pack(anchor="w", padx=15)
        e = tk.Entry(middle)
        e.pack(fill="x", padx=15, pady=4)
        b[key] = e

    b_field("Title", "title")
    b_field("Author", "author")
    b_field("Subject", "subject")
    b_field("Publisher", "publisher")
    b_field("Edition", "edition")
    b_field("Year", "year")
    b_field("Pages", "pages")
    b_field("Volume", "volume")

    # ================= RIGHT: ISSUED BOOKS =================
    right = tk.Frame(body, bg="white")
    right.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(right, text="Already Issued Books",
             font=("Segoe UI", 14, "bold"), bg="white").pack(pady=8)

    table = ttk.Treeview(
        right,
        columns=("acc", "title", "card", "date"),
        show="headings"
    )
    table.pack(fill="both", expand=True, padx=10, pady=10)

    for c in ("acc", "title", "card", "date"):
        table.heading(c, text=c.upper())
        table.column(c, width=150)

    def load_issued():
        table.delete(*table.get_children())
        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT acc_no, title, issued_to_card, issue_date
            FROM books
            WHERE is_issued=1
        """)
        for row in cur.fetchall():
            table.insert("", "end", values=row)
        conn.close()

    # ================= ISSUE BOOK =================
    def issue_book():
        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()

        cur.execute("""
            UPDATE books SET
                is_issued=1,
                issued_to_card=?,
                issue_date=?,
                issue_remarks=?
            WHERE acc_no=? AND is_issued=0
        """, (
            card_no.get(),
            issue_date.get(),
            header_remark.get(),
            acc_no.get()
        ))

        conn.commit()
        conn.close()
        load_issued()
        messagebox.showinfo("Success", "Book Issued Successfully")

    tk.Button(
        win, text="ISSUE BOOK",
        bg="#1e3c72", fg="white",
        font=("Segoe UI", 12, "bold"),
        command=issue_book
    ).pack(pady=10)

    tk.Button(
        win,
        text="Close",
        bg="red",
        fg="white",
        width=10,
        command=win.destroy
    ).pack(pady=10)


    load_issued()
