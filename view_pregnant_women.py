from tkinter import *
from tkinter import ttk
import tkinter as tk
import services # Custom lib

from tkinter import messagebox
import sqlite3

# import database as db
import log

root = Tk()
root.title("View Pregnant Women - AMAS")
root.iconbitmap("img/favicon.png")
root.geometry("1300x400")


style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Open Sans', 11)) # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Open Sans', 13,'bold')) # Modify the font of the headings
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8",), show='headings', style="mystyle.Treeview")
tree.column("#1", anchor=tk.W, width=150)
tree.heading("#1", anchor=tk.W, text="Firstname")
tree.column("#2", anchor=tk.W, width=150)
tree.heading("#2", anchor=tk.W, text="Lastname")
tree.column("#3", anchor=tk.W, width=150)
tree.heading("#3", anchor=tk.W, text="Phone Number")
tree.column("#4", anchor=tk.W, width=150)
tree.heading("#4", anchor=tk.W, text="LMP")
tree.column("#5", anchor=tk.W, width=150)
tree.heading("#5", anchor=tk.W, text="Cycle Length")
tree.column("#6", anchor=tk.W, width=150)
tree.heading("#6", anchor=tk.W, text="Unique ID")
tree.column("#7", anchor=tk.W, width=150)
tree.heading("#7", anchor=tk.W, text="Reg. Date")
tree.column("#8", anchor=tk.W, width=150)
tree.heading("#8", anchor=tk.W, text="Next Appoint.")

tree.tag_configure('odd', background='#E8E8E8')
tree.tag_configure('even', background='#DFDFDF')

# tree.column("#2", anchor=tk.CENTER)
# tree.heading("#2", text="Delete")

tree.grid(row=0, column=0, padx=20, pady=20, ipadx=5, ipady=5)

def view():
    con = sqlite3.connect("db/amas.db")
    c = con.cursor()
    c.execute("SELECT *, oid FROM pregnantwomen")
    rows = c.fetchall() 

    for row in rows:    
        tree.insert("", tk.END, values=row, iid = row[8])           

    c.close()

view()

def onlick_refresh():
    for item in tree.get_children():
        tree.delete(item)
    view()

def onlick_edit_selected():
    row_id = tree.focus()
    
    if row_id == "":
        messagebox.showwarning("Warning", "Empty selection - Kindly select a record to edit!")
        return

    services.pregnant_woman_ID = row_id
    
    import edit_pregnant_woman
    

def onlick_delete_selected():

    row_id = tree.focus()

    if row_id == "":
        messagebox.showwarning("Warning", "Empty selection - Kindly select a record to delete!")
        return

    try:        
        conn = sqlite3.connect("db/amas.db")
        c = conn.cursor()
        c.execute("DELETE from pregnantwomen WHERE oid=" + row_id)
        
        # Commit Changes And Close Connection
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Record Deleted!")

    except ValueError as e:
        messagebox.showwarning("Warning", "ValueError: " + e) 
    except sqlite3.OperationalError:
        messagebox.showwarning("Warning", "Error: sqlite3.OperationalError")
    except Exception as e:
        messagebox.showwarning("Warning", "Error: " + e)

    tree.delete(*tree.get_children())
    view()
    
frame_buttons = LabelFrame(root, text = "Available Actions")
frame_buttons.grid(row=1, column=0, columnspan=2, padx=5, pady=5, ipady=10, ipadx=10)

btn_refresh = Button(frame_buttons, text="Refresh", command=onlick_refresh)
btn_refresh.grid(row=0, column=0, padx=10, pady=5, ipady=5, ipadx=40)

btn_edit = Button(frame_buttons, text="Edit", command=onlick_edit_selected)
btn_edit.grid(row=0, column=1, padx=10, pady=5, ipady=5, ipadx=50)

btn_delete = Button(frame_buttons, text="Delete", command=onlick_delete_selected)
btn_delete.grid(row=0, column=2,  padx=10, pady=5, ipady=5, ipadx=40)

# Close Window
btn_close = Button(frame_buttons, text="Close", command=root.destroy)
btn_close.grid(row=0, column=3, pady=5, padx=10, ipadx=40, ipady=5)

# btn_display.pack(pady=10)


root.mainloop()





