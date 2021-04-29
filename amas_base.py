from tkinter import *
import tkinter as tk
from tkinter import messagebox
import sqlite3

root = Tk()
root.title("AMAS")
root.iconbitmap("img/favicon.png")
root.geometry("600x500")

def onclick_adduser():
    import add_user

def onclick_viewuser():
    import view_users

def onclick_add_pregnant_woman():
    import add_pregnant_woman

def onclick_view_pregnant_women():
    import view_pregnant_women
    

def onclick_login_bypass():
    frame_login.grid_forget()
    frame_authenticated.grid(row=0, column=0, columnspan=2, pady=10, padx=5, ipadx=100, ipady=5)

def onclick_login():
    is_authenticated = False

    con = sqlite3.connect("db/amas.db")
    c = con.cursor()
    c.execute("SELECT * FROM users")
    records = c.fetchall() 

    for username, password in records:    
        if username == entry_username.get() and password == entry_password.get():
            is_authenticated = True

    c.close()

    if is_authenticated == True:
        frame_login.grid_forget()

        frame_authenticated.grid(row=0, column=0, columnspan=2, pady=10, padx=5, ipadx=10, ipady=5)
    else:
        messagebox.showwarning("Warning", "Incorrect details, please try again")
   


# Create Login Frame
frame_login = LabelFrame(root, text="Login", padx=50, pady = 50)
frame_login.grid(row=0, column=0, columnspan=2, pady=15, padx=15, ipadx=10, ipady=5)

# Create Login Form
entry_username = Entry(frame_login, width=50)
entry_username.grid(row=0, column=1, padx=20, pady=(10, 0), ipadx=5, ipady=5)

entry_password = Entry(frame_login, show="*", width=50)
entry_password.grid(row=1, column=1, padx=20, ipadx=5, ipady=5)

# Create Text Box Labels
label_username = Label(frame_login, text="Username")
label_username.grid(row=0, column=0, pady=(10, 0))

label_password = Label(frame_login, text="Password")
label_password.grid(row=1, column=0)
 
# Create Login Button
btn_login = Button(frame_login, text="Login", command=onclick_login)
btn_login.grid(row=3, column=0, columnspan=2, pady=10, padx=20, ipadx=120, ipady=5)

btn_login_bypass = Button(frame_login, text="Bypass", command=onclick_login_bypass)
btn_login_bypass.grid(row=4, column=0, columnspan=2, pady=10, padx=20, ipadx=120, ipady=5)


# Authenticated Section

# Create Frame for Authenticated Users
welcome_text = "Welcome " + entry_username.get()
frame_authenticated = LabelFrame(root, text=welcome_text, padx=50, pady = 50)
frame_authenticated.grid(row=0, column=0, columnspan=2, pady=10, padx=5, ipadx=10, ipady=5)
frame_authenticated.grid_forget()

# Create Add User Button
btn_add_user = Button(frame_authenticated, text="Add New User", command=onclick_adduser)
btn_add_user.grid(row=0, column=0, columnspan=2, pady=10, padx=5, ipadx=100, ipady=5)

# Create View User Button
btn_view_user = Button(frame_authenticated, text="View Users", command=onclick_viewuser)
btn_view_user.grid(row=1, column=0, columnspan=2, pady=10, padx=5, ipadx=110, ipady=5)


# Create Add Pregnant Woman Button
btn_add_pregnant_woman = Button(frame_authenticated, text="Add Pregnant Woman", command=onclick_add_pregnant_woman)
btn_add_pregnant_woman.grid(row=2, column=0, columnspan=2, pady=10, padx=5, ipadx=80, ipady=5)

# Create View Pregnant Women  Button
btn_view_pregnant_women = Button(frame_authenticated, text="View Pregnant Women", command=onclick_view_pregnant_women)
btn_view_pregnant_women.grid(row=3, column=0, columnspan=2, pady=10, padx=5, ipadx=77, ipady=5) 







# Close Window
btn_close = Button(root, text="Close", command=root.destroy)
btn_close.grid(row=4, column=0, columnspan=2, pady=5, padx=5, ipadx=125, ipady=5)





root.mainloop()