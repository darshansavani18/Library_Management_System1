import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def open_member_entry(root):
    win = tk.Toplevel(root)
    win.title("Members")
    win.state("zoomed")
    win.configure(bg="#f2f4f8")

    # ================= MAIN CONTAINER =================
    main_frame = tk.Frame(win, bg="#f2f4f8")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ================= LEFT: ENTRY FORM =================
    left_container = tk.Frame(main_frame, bg="white", width=450)
    left_container.pack(side="left", fill="y", padx=(0, 15))
    left_container.pack_propagate(False)

    canvas = tk.Canvas(left_container, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(left_container, orient="vertical", command=canvas.yview)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    left = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=left, anchor="nw")

    left.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    tk.Label(
        left,
        text="Member Entry",
        font=("Segoe UI", 18, "bold"),
        fg="#1e3c72",
        bg="white"
    ).pack(pady=15)

    group_var = tk.StringVar()
    sit_var = tk.StringVar()
    entries = {}
    selected_id = {"id": None}

    def form_label(text):
        tk.Label(left, text=text, bg="white").pack(anchor="w", padx=20, pady=(5, 0))

    def form_entry(key):
        e = tk.Entry(left)
        e.pack(fill="x", padx=20, pady=5)
        entries[key] = e

    # -------- FORM FIELDS --------
    form_label("Group Name")
    ttk.Combobox(
        left, textvariable=group_var,
        values=["Student", "Staff", "External"],
        state="readonly"
    ).pack(fill="x", padx=20, pady=5)

    form_label("Card No");        form_entry("card_no")
    form_label("Roll No");        form_entry("rno")
    form_label("Member Name");    form_entry("member_name")
    form_label("Father Name");    form_entry("father_name")
    form_label("Address");        form_entry("address")
    form_label("City/Village");   form_entry("city")
    form_label("District/State"); form_entry("district")
    form_label("Department");     form_entry("department")
    form_label("Contact No 1");   form_entry("contact1")
    form_label("Contact No 2");   form_entry("contact2")
    form_label("Remarks");        form_entry("remarks")
    form_label("Valid Date");     form_entry("valid_date")

    form_label("Sitting Plan")
    ttk.Combobox(
        left, textvariable=sit_var,
        values=["Reading Hall", "Reference", "General"],
        state="readonly"
    ).pack(fill="x", padx=20, pady=5)

    # -------- SAVE / UPDATE MEMBER --------
    def save_member():
        data = (
            group_var.get(),
            entries["card_no"].get(),
            entries["rno"].get(),
            entries["member_name"].get(),
            entries["father_name"].get(),
            entries["address"].get(),
            entries["city"].get(),
            entries["district"].get(),
            entries["department"].get(),
            entries["contact1"].get(),
            entries["contact2"].get(),
            sit_var.get(),
            entries["remarks"].get(),
            entries["valid_date"].get()
        )

        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()

        if selected_id["id"] is None:
            cur.execute("""
                INSERT INTO members(
                    group_name, card_no, rno, member_name, father_name,
                    address, city, district, department,
                    contact1, contact2, sitting_plan, remarks, valid_date
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, data)
            messagebox.showinfo("Success", "Member Added")
        else:
            cur.execute("""
                UPDATE members SET
                    group_name=?, card_no=?, rno=?, member_name=?, father_name=?,
                    address=?, city=?, district=?, department=?,
                    contact1=?, contact2=?, sitting_plan=?, remarks=?, valid_date=?
                WHERE id=?
            """, data + (selected_id["id"],))
            messagebox.showinfo("Success", "Member Updated")
            selected_id["id"] = None

        conn.commit()
        conn.close()
        clear_form()
        load_members()

    def clear_form():
        group_var.set("")
        sit_var.set("")
        for e in entries.values():
            e.delete(0, tk.END)

    tk.Button(
        left,
        text="SAVE / UPDATE MEMBER",
        bg="#1e3c72",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        command=save_member
    ).pack(pady=15)

    # ================= RIGHT: MEMBERS LIST =================
    right = tk.Frame(main_frame, bg="white")
    right.pack(side="left", fill="both", expand=True)

    tk.Label(
        right,
        text="Members List",
        font=("Segoe UI", 18, "bold"),
        fg="#1e3c72",
        bg="white"
    ).pack(pady=10)

    # -------- SEARCH BAR --------
    search_var = tk.StringVar()
    search_frame = tk.Frame(right, bg="white")
    search_frame.pack(pady=5)

    tk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left", padx=5)

    # -------- TABLE --------
    table_frame = tk.Frame(right, bg="white")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = (
        "id","group_name","card_no","rno","member_name","father_name",
        "address","city","district","department",
        "contact1","contact2","sitting_plan","remarks","valid_date"
    )

    member_table = ttk.Treeview(table_frame, columns=columns, show="headings")
    member_table.pack(fill="both", expand=True)

    for col in columns:
        member_table.heading(col, text=col.upper())
        member_table.column(col, width=150)

    # -------- LOAD MEMBERS --------
    def load_members():
        member_table.delete(*member_table.get_children())
        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM members")
        for row in cur.fetchall():
            member_table.insert("", "end", values=row)
        conn.close()

    # -------- SEARCH --------
    def search_member():
        member_table.delete(*member_table.get_children())
        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM members
            WHERE member_name LIKE ? OR card_no LIKE ?
        """, (f"%{search_var.get()}%", f"%{search_var.get()}%"))
        for row in cur.fetchall():
            member_table.insert("", "end", values=row)
        conn.close()

    tk.Button(search_frame, text="Search", command=search_member).pack(side="left", padx=5)
    tk.Button(search_frame, text="Show All", command=load_members).pack(side="left", padx=5)

    # -------- SELECT → LOAD INTO FORM --------
    def on_select(event):
        selected = member_table.selection()
        if not selected:
            return
        values = member_table.item(selected)["values"]
        selected_id["id"] = values[0]

        group_var.set(values[1])
        entries["card_no"].delete(0, tk.END); entries["card_no"].insert(0, values[2])
        entries["rno"].delete(0, tk.END); entries["rno"].insert(0, values[3])
        entries["member_name"].delete(0, tk.END); entries["member_name"].insert(0, values[4])
        entries["father_name"].delete(0, tk.END); entries["father_name"].insert(0, values[5])
        entries["address"].delete(0, tk.END); entries["address"].insert(0, values[6])
        entries["city"].delete(0, tk.END); entries["city"].insert(0, values[7])
        entries["district"].delete(0, tk.END); entries["district"].insert(0, values[8])
        entries["department"].delete(0, tk.END); entries["department"].insert(0, values[9])
        entries["contact1"].delete(0, tk.END); entries["contact1"].insert(0, values[10])
        entries["contact2"].delete(0, tk.END); entries["contact2"].insert(0, values[11])
        sit_var.set(values[12])
        entries["remarks"].delete(0, tk.END); entries["remarks"].insert(0, values[13])
        entries["valid_date"].delete(0, tk.END); entries["valid_date"].insert(0, values[14])

    member_table.bind("<<TreeviewSelect>>", on_select)

    # -------- DELETE --------
    def delete_member():
        selected = member_table.selection()
        if not selected:
            messagebox.showerror("Error", "Select a member")
            return
        mid = member_table.item(selected)["values"][0]

        if not messagebox.askyesno("Confirm", "Delete this member?"):
            return

        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM members WHERE id=?", (mid,))
        conn.commit()
        conn.close()
        load_members()

    tk.Button(
        right,
        text="DELETE SELECTED MEMBER",
        bg="red",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=delete_member
    ).pack(pady=10)

    tk.Button(
        win,
        text="Close",
        bg="red",
        fg="white",
        width=10,
        command=win.destroy
    ).pack(pady=10)


    load_members()
