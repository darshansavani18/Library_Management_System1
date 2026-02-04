import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_book_ledger(root):
    win = tk.Toplevel(root)
    win.title("Book Ledger")
    win.state("zoomed")
    win.configure(bg="#f2f4f8")

    # ================= HEADER =================
    header = tk.Frame(win, bg="white", height=90)
    header.pack(fill="x")

    card_no = tk.StringVar()
    from_date = tk.StringVar()
    to_date = tk.StringVar()
    name = tk.StringVar()
    group = tk.StringVar()
    rno = tk.StringVar()

    def h_field(lbl, var, col):
        tk.Label(header, text=lbl, bg="white")\
            .grid(row=0, column=col*2, padx=10, pady=10, sticky="w")
        tk.Entry(header, textvariable=var, width=18)\
            .grid(row=0, column=col*2+1, padx=10)

    h_field("Card No", card_no, 0)
    h_field("From Date", from_date, 1)
    h_field("To Date", to_date, 2)
    h_field("Name", name, 3)
    h_field("Group", group, 4)
    h_field("Roll No", rno, 5)

    # ================= TABLE =================
    table_frame = tk.Frame(win, bg="white")
    table_frame.pack(fill="both", expand=True, padx=15, pady=10)

    x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
    y_scroll = tk.Scrollbar(table_frame, orient="vertical")

    columns = (
        "date", "acc_no", "title", "author",
        "subject", "publisher", "edition"
    )

    ledger_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        xscrollcommand=x_scroll.set,
        yscrollcommand=y_scroll.set
    )

    x_scroll.config(command=ledger_table.xview)
    y_scroll.config(command=ledger_table.yview)

    x_scroll.pack(side="bottom", fill="x")
    y_scroll.pack(side="right", fill="y")
    ledger_table.pack(fill="both", expand=True)

    headings = [
        "Issue Date", "Acc No", "Title",
        "Author", "Subject", "Publisher", "Edition"
    ]

    for col, head in zip(columns, headings):
        ledger_table.heading(col, text=head)
        ledger_table.column(col, width=160, anchor="center")

    ledger_table.column("title", width=260, anchor="w")

    # ================= LOAD LEDGER =================
    def load_ledger():
        ledger_table.delete(*ledger_table.get_children())

        if card_no.get() == "":
            messagebox.showwarning("Error", "Enter Card No")
            return

        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()

        query = """
            SELECT 
                i.issue_date,
                b.acc_no,
                b.title,
                b.author,
                b.sub,
                b.publisher,
                b.edition
            FROM issue_books i
            JOIN books b ON i.acc_no = b.acc_no
            JOIN members m ON i.card_no = m.card_no
            WHERE i.card_no = ?
        """

        params = [card_no.get()]

        if from_date.get() and to_date.get():
            query += " AND i.issue_date BETWEEN ? AND ?"
            params.extend([from_date.get(), to_date.get()])

        cur.execute(query, params)
        rows = cur.fetchall()

        # Load student details
        cur.execute("""
            SELECT member_name, group_name, rno
            FROM members
            WHERE card_no=?
        """, (card_no.get(),))

        stu = cur.fetchone()
        if stu:
            name.set(stu[0])
            group.set(stu[1])
            rno.set(stu[2])

        conn.close()

        for row in rows:
            ledger_table.insert("", "end", values=row)

    # ================= BUTTON =================
    tk.Button(
        header,
        text="Search",
        bg="#1e3c72",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=load_ledger
    ).grid(row=0, column=12, padx=20)

