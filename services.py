from tkinter import *
from tkinter import messagebox
import sqlite3
import random
import datetime


import database as db
import log

# Variable for pregnant woman ID
global pregnant_woman_ID
# global pregnant_woman_updates = False


# db.create_user_table()

def generate_uniqueID(firstname, lastname):
    uniqueID = firstname[0] + lastname[0] + str(random.randint(111, 999))
    return uniqueID.upper()

def nextappointment_calculator(LMP, cyclelength=28):

    pregnant_age_days = (datetime.date.today() - LMP).days
    pregnant_age_weeks = int(pregnant_age_days) / 7

    next_appointment = datetime.datetime.today()

    if pregnant_age_weeks <= 12:
        next_appointment = LMP + datetime.timedelta(weeks=12)
    elif 12 < pregnant_age_weeks <= 16:
        next_appointment = LMP + datetime.timedelta(weeks=16)
    elif 16 < pregnant_age_weeks <= 20:
        next_appointment = LMP + datetime.timedelta(weeks=20)
    elif 20 < pregnant_age_weeks <= 24:
        next_appointment = LMP + datetime.timedelta(weeks=24)
    elif 24 < pregnant_age_weeks <= 28:
        next_appointment = LMP + datetime.timedelta(weeks=28)
    elif 28 < pregnant_age_weeks <= 30:
        next_appointment = LMP + datetime.timedelta(weeks=30)
    elif 30 < pregnant_age_weeks <= 32:
        next_appointment = LMP + datetime.timedelta(weeks=32)
    elif 32 < pregnant_age_weeks <= 34:
        next_appointment = LMP + datetime.timedelta(weeks=34)
    elif 34 < pregnant_age_weeks <= 36:
        next_appointment = LMP + datetime.timedelta(weeks=36)
    elif 36 < pregnant_age_weeks <= 37:
        next_appointment = LMP + datetime.timedelta(weeks=37)
    elif 37 < pregnant_age_weeks <= 38:
        next_appointment = LMP + datetime.timedelta(weeks=38)
    elif 38 < pregnant_age_weeks <= 39:
        next_appointment = LMP + datetime.timedelta(weeks=39)
    elif 39 < pregnant_age_weeks <= 40:
        next_appointment = LMP + datetime.timedelta(weeks=37)
    else:
        next_appointment = datetime.date.today()  
    
    return next_appointment
