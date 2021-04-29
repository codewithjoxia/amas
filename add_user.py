from tkinter import *
from tkinter import messagebox
import sqlite3

import database as db
import log

root = Tk()
root.title("Add User - AMAS")
root.iconbitmap("img/favicon.png")
root.geometry("450x200")

# db.create_user_table()

def onclick_submit():

    if username.get().strip() == "" or password.get().strip() == "":
        messagebox.showwarning("Warning", "Cannot accept empty fields")
        return

    try:
        conn = sqlite3.connect('db/amas.db')
        # Create cursor
        c = conn.cursor()

        c.execute("SELECT * FROM users")
        records = c.fetchall()

        username_exists = False
        for record in records:
            print (record)   
            if username.get().strip() == record[0].strip():
                username_exists = True            
            
        if username_exists == False:
                       
            # Insert Into Table
            c.execute("INSERT INTO users VALUES(:username, :password)",
                        {
                            'username': username.get(),
                            'password': password.get(),                    
                        }                
                    )

                        
            messagebox.showinfo("Success", username.get() + " was added!")

            # Commit Changes
            conn.commit()
            # Close Connection
            conn.close()

            # Clear The Text Boxes
            username.delete(0, END)
            password.delete(0, END)
        else:
            messagebox.showwarning("Warning", username.get() + " already exist, try another username!") 

    except IOError:
        raise RuntimeError
        messagebox.showerror("Error", "An error occured while saving user" + str(sys.exc_info()[0])) 
        
        log.error_log("Error adding new user")   


# Create Text Boxes
username = Entry(root, width=50,)
username.grid(row=0, column=1, padx=20, pady=(10, 0), ipadx=5, ipady=5)

password = Entry(root, show="*", width=50)
password.grid(row=1, column=1, padx=20, ipadx=5, ipady=5)

# Create Text Box Labels
username_label = Label(root, text="Username")
username_label.grid(row=0, column=0, pady=(10, 0), ipadx=5, ipady=5)

password_label = Label(root, text="Password")
password_label.grid(row=1, column=0, ipadx=5, ipady=5)

# Create Submit Button
btn_submit = Button(root, text="Add New User", command=onclick_submit)
btn_submit.grid(row=2, column=0, columnspan=2, pady=10, padx=5, ipadx=80, ipady=5)

# Close Window
btn_close = Button(root, text="Close", command=root.destroy)
btn_close.grid(row=3, column=0, columnspan=2, pady=5, padx=5, ipadx=105, ipady=5)

root.mainloop()