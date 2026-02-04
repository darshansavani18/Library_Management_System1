import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

def open_list_books(root):
    win = tk.Toplevel(root)
    win.title("List of Books")
    win.state("zoomed")
    win.configure(bg="#f2f4f8")

    tk.Label(
        win,
        text="List of Books",
        font=("Segoe UI", 22, "bold"),
        fg="#1e3c72",
        bg="#f2f4f8"
    ).pack(pady=15)
# ================= SEARCH PANEL =================
    search_frame = tk.Frame(win, bg="#f2f4f8")
    search_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(
    search_frame,
    text="Search By:",
    bg="#f2f4f8",
    font=("Segoe UI", 11, "bold")
    ).pack(side="left", padx=(0, 10))

    search_by = tk.StringVar()
    search_combo = ttk.Combobox(
        search_frame,
        textvariable=search_by,
        state="readonly",
        width=18,
        values=[
            "acc_no", "title", "author", "publisher",
            "isbn", "location", "topic", "sub"
        ]
    )
    search_combo.current(1)   # default = title
    search_combo.pack(side="left", padx=5)

    search_entry = tk.Entry(
        search_frame,
        font=("Segoe UI", 11),
        width=30    
    )
    search_entry.pack(side="left", padx=10)
    

    table_frame = tk.Frame(win, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
    y_scroll = tk.Scrollbar(table_frame, orient="vertical")

    columns = (
        "id", "acc_no", "bar_code", "title", "author", "publisher",
        "topic", "sub", "edition", "year", "no_page", "volume",
        "source", "bill_no", "bill_date", "e_cost", "class",
        "b_no", "isbn", "location", "remarks"
    )

    book_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        xscrollcommand=x_scroll.set,
        yscrollcommand=y_scroll.set
    )

    x_scroll.config(command=book_table.xview)
    y_scroll.config(command=book_table.yview)

    x_scroll.pack(side="bottom", fill="x")
    y_scroll.pack(side="right", fill="y")
    book_table.pack(fill="both", expand=True)

    headings = [
        "ID", "Acc No", "Bar Code", "Title", "Author", "Publisher",
        "Topic", "Subject", "Edition", "Year", "Pages", "Volume",
        "Source", "Bill No", "Bill Date", "Cost", "Class",
        "Book No", "ISBN", "Location", "Remarks"
    ]

    for col, head in zip(columns, headings):
        book_table.heading(col, text=head)
        book_table.column(col, width=130, anchor="center")

    book_table.column("title", width=260, anchor="w")
    book_table.column("remarks", width=260, anchor="w")

    # ---------- LOAD DATA ----------
    def load_books(where_clause=None, params=()):
        book_table.delete(*book_table.get_children())

        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()

        if where_clause:
            cur.execute(f"SELECT * FROM books WHERE {where_clause}", params)
        else:
            cur.execute("SELECT * FROM books")

        rows = cur.fetchall()
        conn.close()

        for row in rows:
            book_table.insert("", "end", values=row)
    load_books()
    def search_books():
        field = search_by.get()
        value = search_entry.get()

        if field == "" or value == "":
            messagebox.showwarning("Warning", "Select field and enter value")
            return

        load_books(f"{field} LIKE ?", (f"%{value}%",))

    def reset_search():
        search_entry.delete(0, tk.END)
        load_books()
    tk.Button(
    search_frame,
    text="SEARCH",
    bg="#1e3c72",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=10,
    command=search_books
    ).pack(side="left", padx=5)

    tk.Button(
    search_frame,
    text="RESET",
    bg="#7f8c8d",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=10,
    command=reset_search
    ).pack(side="left", padx=5)

    # ---------- GET SELECTED BOOK ----------
    def get_selected_book():
        selected = book_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book first")
            return None
        return book_table.item(selected)["values"]

    # ---------- DELETE BOOK ----------
    def delete_book():
        data = get_selected_book()
        if not data:
            return

        book_id = data[0]

        confirm = messagebox.askyesno("Confirm Delete", "Delete selected book?")
        if confirm:
            conn = sqlite3.connect("LMS.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()
            conn.close()

            load_books()
            messagebox.showinfo("Success", "Book Deleted")

    # ---------- UPDATE BOOK ----------
    def update_book():
        data = get_selected_book()
        if not data:
            return

        edit = tk.Toplevel(win)
        edit.title("Update Book")
        edit.geometry("500x600")
        edit.configure(bg="#f2f4f8")

        fields = columns[1:]  # exclude id
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(edit, text=field.upper(), bg="#f2f4f8")\
                .grid(row=i, column=0, padx=15, pady=5, sticky="w")

            ent = tk.Entry(edit, width=40)
            ent.grid(row=i, column=1, padx=15, pady=5)
            ent.insert(0, data[i+1])

            entries[field] = ent

        def save_update():
            values = [entries[f].get() for f in fields]
            values.append(data[0])  # id at end

            conn = sqlite3.connect("LMS.db")
            cur = conn.cursor()
            cur.execute("""
                UPDATE books SET
                acc_no=?, bar_code=?, title=?, author=?, publisher=?, topic=?, sub=?,
                edition=?, year=?, no_page=?, volume=?, source=?, bill_no=?, bill_date=?,
                e_cost=?, class=?, b_no=?, isbn=?, location=?, remarks=?
                WHERE id=?
            """, values)

            conn.commit()
            conn.close()

            edit.destroy()
            load_books()
            messagebox.showinfo("Success", "Book Updated")

        tk.Button(
            edit,
            text="UPDATE BOOK",
            bg="#1e3c72",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            command=save_update
        ).grid(row=len(fields)+1, column=0, columnspan=2, pady=20)

    # ---------- BUTTONS ----------
    btn_frame = tk.Frame(win, bg="#f2f4f8")
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame,
        text="UPDATE",
        bg="#f39c12",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        width=15,
        command=update_book
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame,
        text="DELETE",
        bg="#e74c3c",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        width=15,
        command=delete_book
    ).pack(side="left", padx=10)


def open_new_book_entry(root):
    win = tk.Toplevel(root)
    win.title("New Book Entry")
    win.state("zoomed")
    win.configure(bg="#f2f4f8")

    canvas = tk.Canvas(win, bg="#f2f4f8")
    scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f2f4f8")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(
        scroll_frame,
        text="New Book Entry",
        font=("Segoe UI", 22, "bold"),
        fg="#1e3c72",
        bg="#f2f4f8"
    ).grid(row=0, column=0, columnspan=4, pady=20)

    fields = [
        ("Accession No", "acc_no"),
        ("Bar Code", "bar_code"),
        ("Title", "title"),
        ("Author", "author"),
        ("Publisher", "publisher"),
        ("Topic", "topic"),
        ("Subject", "sub"),
        ("Edition", "edition"),
        ("Year", "year"),
        ("No of Pages", "no_page"),
        ("Volume", "volume"),
        ("Source", "source"),
        ("Bill No", "bill_no"),
        ("Bill Date", "bill_date"),
        ("Estimated Cost", "e_cost"),
        ("Class", "class"),
        ("Book No", "b_no"),
        ("ISBN", "isbn"),
        ("Location", "location"),
        ("Remarks", "remarks")
    ]

    entries = {}

    row = 1
    col = 0

    for label, key in fields:
        tk.Label(scroll_frame, text=label, bg="#f2f4f8",
                 font=("Segoe UI", 11)).grid(row=row, column=col, padx=20, pady=8, sticky="w")

        ent = tk.Entry(scroll_frame, width=30, font=("Segoe UI", 11))
        ent.grid(row=row, column=col+1, padx=20, pady=8)

        entries[key] = ent

        col += 2
        if col == 4:
            col = 0
            row += 1

    def save_book():
        data = [entries[k].get() for _, k in fields]

        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO books(
            acc_no, bar_code, title, author, publisher, topic, sub,
            edition, year, no_page, volume, source, bill_no, bill_date,
            e_cost, class, b_no, isbn, location, remarks
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, data)

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Book Added Successfully")
        win.destroy()

    tk.Button(
        scroll_frame,
        text="SAVE BOOK",
        bg="#1e3c72",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        width=20,
        command=save_book
    ).grid(row=row+1, column=0, columnspan=4, pady=30)
    tk.Button(
        win,
        text="Close",
        bg="red",
        fg="white",
        width=10,
        command=win.destroy
    ).pack(pady=10)
