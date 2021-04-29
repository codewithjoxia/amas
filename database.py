from tkinter import *
import sqlite3

# root = Tk()
# root.title("Add User - AMAS")
# root.iconbitmap("img/favicon.png")
# root.geometry("500x800")

def open_connection():
    # Create a database or connect to one
    global conn 
    conn = sqlite3.connect('db/amas.db')
    # Create cursor
    c = conn.cursor()
    return c

def close_connection():
    # Commit Changes
    conn.commit()
    # Close Connection
    conn.close()

def select_allusers():
    c = open_connection()

    c.execute("SELECT *, oid FROM users")
    records = c.fetchall()
    close_connection()

    return records

def create_user_table():
    # Create a database or connect to one
    conn = sqlite3.connect('db/amas.db')
    # Create cursor
    c = conn.cursor()

    # Create table  - We only need to do this once
    # '''
    c.execute("""CREATE TABLE users 
                    (
                        username text,
                        password text
                    )
                """)

    # '''

    # Commit Changes
    conn.commit()
    # Close Connection
    conn.close()

# root.mainloop()