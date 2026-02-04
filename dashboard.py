import tkinter as tk
from utils.clock import start_clock
from utils.image_loader import load_image
from ui.members import open_member_entry
from ui.books import open_new_book_entry, open_list_books
from ui.create_user import open_create_user
from ui.issue_book import open_issue_book
from ui.issue_book_regi import open_issued_books_list
from ui.receive_book import open_receive_book
from ui.receive_book_regi import open_receive_books_list
from ui.book_ledger import open_book_ledger
from ui.pending_book import open_pending_books
from ui.group import open_group_module
from tkinter import messagebox

def open_dashboard(root,on_login_show,role):
    desh = tk.Toplevel(root)
    desh.state("zoomed")
    desh.title("Library dashboard")

    w = desh.winfo_screenwidth()
    h = desh.winfo_screenheight()

    # LEFT PANEL (same as before)
    left_panel = tk.Frame(desh, bg="#1e3c72", width=int(w*0.45), height=h)
    left_panel.place(x=0, y=0)
    # ---------- TITLE ----------
    tk.Label(
    left_panel,
    text="My Library",
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg="#1e3c72"
).pack(pady=30)

# ---------- MENU BUTTON FACTORY ----------

    def menu_btn(text, command=None):
        btn =  tk.Button(
        left_panel,
        text=text,
        font=("Segoe UI", 15, "bold"),
        fg="white",
        bg="#1e3c72",
        activebackground="#2a5298",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=command
    )
        btn.pack(fill="x", padx=20, pady=10)
        btn.bind("<Enter>", lambda e: btn.config(bg="#2a5298"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#1e3c72"))

        return btn
# ---------- MENU BUTTONS ----------
    if role=="admin":
        menu_btn("New Book Entry", command=lambda: open_new_book_entry(desh)).pack(pady=2)
        menu_btn("List of Books", command=lambda: open_list_books(desh)).pack(pady=2)
        menu_btn("Members", command=lambda: open_member_entry(desh)).pack(pady=2)
        menu_btn("Issue Book", command=lambda: open_issue_book(desh)).pack(pady=2)
        menu_btn("Receive Book", command=lambda: open_receive_book(desh)).pack(pady=2)
        menu_btn("Issue Register", command=lambda: open_issued_books_list(desh)).pack(pady=2)
        menu_btn("Receive Register", command=lambda: open_receive_books_list(desh)).pack(pady=2)
        menu_btn("Book Ledger", command=lambda: open_book_ledger(desh)).pack(pady=2)
        menu_btn("Pending Books", command=lambda: open_pending_books(desh)).pack(pady=2)
        menu_btn("Groups", command=lambda:open_group_module(desh)).pack(pady=2)
        tk.Button(
            left_panel,
            text="Create New User",
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#1e3c72",
            bd=0,
            cursor="hand2",
            command=lambda: open_create_user(desh)
        ).pack(fill="x", padx=20, pady=(30,15))
    else:
        menu_btn("List of Books", command=lambda: open_list_books(desh)).pack(pady=20)
        menu_btn("Issue Book", command=lambda: open_issue_book(desh)).pack(pady=20)
        menu_btn("Receive Book", command=lambda: open_receive_book(desh)).pack(pady=20)
        menu_btn("Book Ledger", command=lambda: open_book_ledger(desh)).pack(pady=20)
        menu_btn("Pending Books", command=lambda: open_pending_books(desh)).pack(pady=20)

    # CLOCK (same position)
    clock_label = tk.Label(left_panel, fg="white", bg="#1e3c72",
                           font=("Segoe UI", 14, "bold"))
    clock_label.pack(pady=(5,20))
    start_clock(clock_label)
    def logout():
        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )
        if confirm:
            desh.destroy()          # close dashboard safely
            root.deiconify()
            root.state("zoomed")
            root.lift()
            root.focus_force()

            on_login_show()

    logout_border = tk.Frame(
        left_panel,
        bg="#ffffff",
        padx=1,
        pady=1
    )
    logout_border.pack(fill="x", padx=15, pady=(5, 10))

    logout_frame = tk.Frame(
        logout_border,
        bg="#1e3c72"
    )
    logout_frame.pack(fill="x")

    tk.Button(
        logout_frame,
        text="Logout",
        font=("Segoe UI", 13, "bold"),
        fg="white",
        bg="red",
        activebackground="#c0392b",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=logout
    ).pack(fill="x", padx=10, pady=8)

    # MAIN AREA (same)
    main_area = tk.Frame(desh, bg="#f2f4f8",
                         width=int(w*0.75), height=h)
    main_area.place(x=int(w*0.25), y=0)

    # IMAGE (same)
    img = load_image("assets/image2.jpg", (900,700))
    img_label = tk.Label(main_area, image=img, bg="white")
    img_label.image = img
    img_label.pack(expand=True,anchor="n", pady=(40,0))

    
    desh.mainloop()
