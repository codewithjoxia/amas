from tkinter import *
from tkinter import messagebox
import sqlite3
import random
import datetime
import services # Custom lib

from tkcalendar import Calendar #Installed using pip3 install tkcalendar

import database as db
import log

root = Tk()
root.title("Edit Pregnant Woman - AMAS")
root.iconbitmap("img/favicon.png")
root.geometry("500x500")

global record_id 
record_id = services.pregnant_woman_ID

# Create a function to update the recorcd

def onclick_edit():
    next_appointment = services.nextappointment_calculator(calendar_LMP.selection_get(), spinbox_cycle_length.get())
    
    if entry_firstname.get().strip() == "" or entry_lastname.get().strip() == "" or entry_phonenumber.get().strip() == "":
        messagebox.showwarning("Warning", "Cannot accept empty fields")
        return

    
    if calendar_LMP.selection_get() == datetime.date.today():
        messagebox.showwarning("Warning", "You can't select today's date")
        return

    next_appointment = services.nextappointment_calculator(calendar_LMP.selection_get(), spinbox_cycle_length.get())

    try:
       # Create a database or connect to one
        conn = sqlite3.connect('db/amas.db')
        # Create cursor
        c = conn.cursor()

        # record_id = services.pregnant_woman_ID # record ID from previous windows

        c.execute("""UPDATE pregnantwomen SET
                    firstname = :first,
                    lastname = :last,
                    phonenumber = :phone,
                    LMP = :LM,
                    cyclelength = :cycle

                    WHERE oid = :oid_ID   
                    """,
                    {
                        'first' : entry_firstname.get(),
                        'last' : entry_lastname.get(),
                        'phone' : entry_phonenumber.get(),
                        'LM' : calendar_LMP.selection_get(),
                        'cycle' : spinbox_cycle_length.get(),
                        'oid_ID': record_id
                    }
                
                )

        # Commit Changes
        conn.commit()
        # Close Connection
        conn.close()

        messagebox.showinfo("Success", entry_firstname.get() + " " + " was edited")
        # import view_pregnant_women
        root.destroy()
        

    except IOError as e:
        raise RuntimeError
        messagebox.showerror("Error", "An error occured while updating " + entry_firstname.get() + " " + str(e) ) #str(sys.exc_info()[0])) 
        
        log.error_log("Error adding new pregnant woman")   

    except AttributeError as e:
        raise RuntimeError
        messagebox.showerror("Error", "An error occured while saving user" + str(e) ) #str(sys.exc_info()[0])) 
        
        log.error_log("Error adding new pregnant woman") 

    except Exception as e:
        
        messagebox.showerror("Error", "An error occured while saving user" + str(e) ) #str(sys.exc_info()[0])) 
        
        log.error_log("Error adding new pregnant woman") 


# Create Text Boxes
entry_firstname = Entry(root, width=50,)
entry_firstname.grid(row=0, column=1, padx=20, pady=(10, 0), ipadx=5, ipady=5)

entry_lastname = Entry(root, width=50)
entry_lastname.grid(row=1, column=1, padx=20, ipadx=5, ipady=5)

entry_phonenumber = Entry(root, width=50,)
entry_phonenumber.grid(row=2, column=1, padx=20, pady=(10, 0), ipadx=5, ipady=5)

# calendar_LMP = Calendar(root, selectmode = 'day') #, year = 2021, month = 5, day = 22)
# calendar_LMP.grid(row=3, column=1, padx=20, pady=(10, 0), ipadx=5, ipady=5)

spinbox_cycle_length = Spinbox(root, from_=27, to=33)
spinbox_cycle_length.grid(row=4, column=1, padx=20, pady=(10, 0), ipadx=5, ipady=5)

# Create Text Box Labels
label_firstname = Label(root, text="Firstname")
label_firstname.grid(row=0, column=0, pady=(10, 0), ipadx=5, ipady=5)

label_lastname = Label(root, text="Lastname")
label_lastname.grid(row=1, column=0, ipadx=5, ipady=5)

label_phonenumber = Label(root, text="Phone Number")
label_phonenumber.grid(row=2, column=0, ipadx=5, ipady=5)

label_LMP = Label(root, text="Date of LMP")
label_LMP.grid(row=3, column=0, ipadx=5, ipady=5)

label_cycle_length = Label(root, text="Cycle Length")
label_cycle_length.grid(row=4, column=0, ipadx=5, ipady=5)

# Create a database or connect to one
conn = sqlite3.connect('db/amas.db')
# Create cursor
c = conn.cursor()

# Query The Database
c.execute("SELECT * FROM pregnantwomen WHERE oid =" + record_id)
records = c.fetchall()

# Loop Through Results
for record in records:
    entry_firstname.insert(0, record[0])
    entry_lastname.insert(0, record[1])
    entry_phonenumber.insert(0, record[2])

    calendar_LMP = Calendar(root, selectmode = 'day', year = int(record[3].split("-")[0]), month = int(record[3].split("-")[1]), day = int(record[3].split("-")[2]))
    calendar_LMP.grid(row=3, column=1, padx=20, pady=(10, 0), ipadx=5, ipady=5)

    spinbox_cycle_length.delete(0, END)
    spinbox_cycle_length.insert(0, record[4])
        

# Create Edit Button
btn_edit = Button(root, text="Edit Pregnant Woman", command=onclick_edit)
btn_edit.grid(row=5, column=1, columnspan=2, pady=10, padx=5, ipadx=80, ipady=5)

# Close Window
btn_close = Button(root, text="Close", command=root.destroy)
btn_close.grid(row=6, column=1, columnspan=2, pady=5, padx=5, ipadx=125, ipady=5)

root.mainloop()