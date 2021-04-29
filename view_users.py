from tkinter import *
from tkinter import ttk
import tkinter as tk

from tkinter import messagebox
import sqlite3

# import database as db
import log

root = Tk()
root.title("View Users - AMAS")
root.iconbitmap("img/favicon.png")
root.geometry("400x400")

# db.create_user_table()

tree = ttk.Treeview(root, column=("c1"), show='headings')
tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text="Username")

# tree.column("#2", anchor=tk.CENTER)
# tree.heading("#2", text="Delete")

tree.grid(row=0, column=0, padx=20, ipadx=5, ipady=5)

def View():
    con = sqlite3.connect("db/amas.db")
    c = con.cursor()
    c.execute("SELECT *, oid FROM users")
    rows = c.fetchall() 

    for row in rows:    
        tree.insert("", tk.END, values=row[0], iid = row[2]) 
          

    c.close()

View()

def onlick_delete_selected():

    try:
        row_id = tree.focus()

        conn = sqlite3.connect("db/amas.db")
        c = conn.cursor()
        c.execute("DELETE from users WHERE oid=" + row_id)
        
        # Commit Changes And Close Connection
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "User Deleted!")
    except ValueError:
        messagebox.showwarning("Warning", "Kindly select a User to delete!") 
    except sqlite3.OperationalError:
        messagebox.showwarning("Warning", "Kindly select a User to delete!")

    tree.delete(*tree.get_children())
    View()
    

btn_delete = Button(root, text="Delete Selected", command=onlick_delete_selected)
btn_delete.grid(row=1, column=0, columnspan=2, padx=5, pady=5, ipady=5, ipadx=60)

# Close Window
btn_close = Button(root, text="Close", command=root.destroy)
btn_close.grid(row=2, column=0, columnspan=2, pady=5, padx=5, ipadx=85, ipady=5)

# btn_display.pack(pady=10)


root.mainloop()





