import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_group_module(root):
    win = tk.Toplevel(root)
    win.title("Groups")
    win.state("zoomed")
    win.configure(bg="#f2f4f8")

    # ================= MAIN FRAME =================
    main = tk.Frame(win, bg="#f2f4f8")
    main.pack(fill="both", expand=True, padx=15, pady=15)

    # ================= LEFT : FORM =================
    left = tk.Frame(main, bg="white", width=350)
    left.pack(side="left", fill="y", padx=5)
    left.pack_propagate(False)

    tk.Label(
        left,
        text="Group Master",
        font=("Segoe UI", 16, "bold"),
        fg="#1e3c72",
        bg="white"
    ).pack(pady=15)

    tk.Label(left, text="Group Name", bg="white").pack(anchor="w", padx=20)
    group_name = tk.Entry(left, font=("Segoe UI", 12))
    group_name.pack(fill="x", padx=20, pady=5)

    tk.Label(left, text="Description", bg="white").pack(anchor="w", padx=20)
    description = tk.Text(left, height=4, font=("Segoe UI", 11))
    description.pack(fill="x", padx=20, pady=5)

    selected_id = tk.StringVar()

    # ================= BUTTONS =================
    btn_frame = tk.Frame(left, bg="white")
    btn_frame.pack(pady=15)

    def clear_form():
        selected_id.set("")
        group_name.delete(0, tk.END)
        description.delete("1.0", tk.END)

    def save_group():
        name = group_name.get().strip()
        desc = description.get("1.0", tk.END).strip()

        if name == "":
            messagebox.showwarning("Error", "Group name required")
            return

        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()

        try:
            if selected_id.get() == "":
                cur.execute(
                    "INSERT INTO groups(group_name, description) VALUES (?,?)",
                    (name, desc)
                )
            else:
                cur.execute(
                    "UPDATE groups SET group_name=?, description=? WHERE id=?",
                    (name, desc, selected_id.get())
                )

            conn.commit()
            messagebox.showinfo("Success", "Group Saved Successfully")
            clear_form()
            load_groups()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Group already exists")

        conn.close()

    tk.Button(
        btn_frame, text="Save",
        bg="#1e3c72", fg="white",
        font=("Segoe UI", 11, "bold"),
        width=10,
        command=save_group
    ).pack(side="left", padx=5)

    tk.Button(
        btn_frame, text="Clear",
        bg="#95a5a6", fg="white",
        font=("Segoe UI", 11, "bold"),
        width=10,
        command=clear_form
    ).pack(side="left", padx=5)

    # ================= RIGHT : TABLE =================
    right = tk.Frame(main, bg="white")
    right.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(
        right,
        text="Group List",
        font=("Segoe UI", 16, "bold"),
        fg="#1e3c72",
        bg="white"
    ).pack(pady=10)

    table = ttk.Treeview(
        right,
        columns=("id", "name", "desc"),
        show="headings"
    )
    table.pack(fill="both", expand=True, padx=10, pady=10)

    table.heading("id", text="ID")
    table.heading("name", text="Group Name")
    table.heading("desc", text="Description")

    table.column("id", width=60, anchor="center")
    table.column("name", width=200)
    table.column("desc", width=400)

    # ================= LOAD GROUPS =================
    def load_groups():
        table.delete(*table.get_children())
        conn = sqlite3.connect("LMS.db")
        cur = conn.cursor()
        cur.execute("SELECT id, group_name, description FROM groups")
        for row in cur.fetchall():
            table.insert("", "end", values=row)
        conn.close()

    # ================= SELECT EVENT =================
    def on_select(event):
        sel = table.focus()
        if not sel:
            return
        row = table.item(sel, "values")
        selected_id.set(row[0])
        group_name.delete(0, tk.END)
        group_name.insert(0, row[1])
        description.delete("1.0", tk.END)
        description.insert("1.0", row[2])

    table.bind("<<TreeviewSelect>>", on_select)

    load_groups()
