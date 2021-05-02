from tkinter import *
from tkinter import messagebox
import sqlite3
import random
import datetime
import services #custom lib

from tkcalendar import Calendar #Installed using pip3 install tkcalendar

import database as db
import log

root = Tk()
root.title("Add Pregnant Woman - AMAS")
root.iconbitmap("img/favicon.png")
root.geometry("500x500")

def onclick_submit():
    next_appointment = services.nextappointment_calculator(calendar_LMP.selection_get(), spinbox_cycle_length.get())
    
    if entry_firstname.get().strip() == "" or entry_lastname.get().strip() == "" or entry_phonenumber.get().strip() == "":
        messagebox.showwarning("Warning", "Cannot accept empty fields")
        return

    
    if calendar_LMP.selection_get() == datetime.date.today():
        messagebox.showwarning("Warning", "You can't select today's date")
        return

    next_appointment = services.nextappointment_calculator(calendar_LMP.selection_get(), spinbox_cycle_length.get())

    uniqueID = services.generate_uniqueID(entry_firstname.get(), entry_lastname.get())

    

    try:
        conn = sqlite3.connect('db/amas.db')
        # Create cursor
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS pregnantwomen 
                    (
                        firstname text NOT NULL,
                        lastname text NOT NULL,
                        phonenumber text NOT NULL,
                        LMP text NOT NULL,
                        cyclelength integer,
                        uniqueID text NOT NULL,
                        registrationdate text NOT NULL,
                        nextappointment text
                    )
                """)

        c.execute("SELECT * FROM pregnantwomen")
        records = c.fetchall()  

        for record in records:            
            if uniqueID == record[5].strip():
                uniqueID = services.generate_uniqueID(entry_firstname.get(), entry_lastname.get())

        
        # Insert Into Table
        c.execute("INSERT INTO pregnantwomen VALUES(:firstname, :lastname, :phonenumber, :LMP, :cyclelength, :uniqueID, :registrationdate, :nextappointment)",
                    {
                        
                        'firstname' : entry_firstname.get(),
                        'lastname' : entry_lastname.get(),
                        'phonenumber' : entry_phonenumber.get(),
                        'LMP' : calendar_LMP.selection_get(),
                        'cyclelength' : spinbox_cycle_length.get(),
                        'uniqueID' : uniqueID,
                        'registrationdate' : datetime.date.today(),
                        'nextappointment' : next_appointment                      
                    }                
                )

        # Commit Changes
        conn.commit()
        # Close Connection
        conn.close()

        messagebox.showinfo("Success", "New pregnant woman added")

        # Clear The Text Boxes
        entry_firstname.delete(0, END)
        entry_lastname.delete(0, END)
        entry_phonenumber.delete(0, END)

    except IOError as e:
        raise RuntimeError
        messagebox.showerror("Error", "An error occured while saving user" + str(e) ) #str(sys.exc_info()[0])) 
        
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

calendar_LMP = Calendar(root, selectmode = 'day') #, year = 2021, month = 5, day = 22)
calendar_LMP.grid(row=3, column=1, padx=20, pady=(10, 0), ipadx=5, ipady=5)

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

# Create Submit Button
btn_submit = Button(root, text="Add Pregnant Woman", command=onclick_submit)
btn_submit.grid(row=5, column=1, columnspan=2, pady=10, padx=5, ipadx=80, ipady=5)

# Close Window
btn_close = Button(root, text="Close", command=root.destroy)
btn_close.grid(row=6, column=1, columnspan=2, pady=5, padx=5, ipadx=125, ipady=5)

root.mainloop()