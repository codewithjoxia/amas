from tkinter import *
from tkinter import messagebox
import sqlite3
import random
import datetime
import requests
import urllib
import json
import database as db
import log

# Variable for pregnant woman ID
global pregnant_woman_ID

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

def load_schedule():
    try:
        conn = sqlite3.connect('db/amas.db')
        # Create cursor
        c = conn.cursor()

        c.execute("SELECT * FROM pregnantwomen")
        records = c.fetchall()  

        for record in records: 
            LMP_date == record[3].strip()

            if datetime.date.today() < LMP + datetime.timedelta(weeks=40):
                nextappointment = nextappointment_calculator(LMP_date, 28)
                if nextappointment == datetime.date.today.timedelta(1):
                    
                    # Save SMS to database
                    c.execute("""CREATE TABLE IF NOT EXISTS sms 
                                (
                                    sms text NOT NULL,
                                    phonenumber text NOT NULL,
                                    datesaved text NOT NULL,
                                    datesent text,                                    
                                    sent text NOT NULL
                                )
                            """)
                    
                    phonenumber = record[2].strip()

                    sms = "Hi {name}, \n\nThis is a friendly reminder for your ANC appointment at our clinic tomorrow {date} by 10am. \n\nThanks"
                    sms = sms.format(name = record[0].strip(), date = nextappointment)
                    
                    # Insert Into Table
                    c.execute("INSERT INTO sms VALUES(:sms, :datesaved, :datesent, :sent)",
                                {                        
                                    'sms' : sms,
                                    'phonenumber' : phonenumber,
                                    'datesaved' : datetime.date.today(),
                                    'sent' : '0'                        
                                }                
                            )

        # Commit Changes
        conn.commit()
        # Close Connection
        conn.close()
        log.error_log("Schedule loaded!")

    except IOError as e:
        raise RuntimeError
        
        log.error_log("Schedule not loaded! " + str(e))
        
    except AttributeError as e:
        raise RuntimeError
        log.error_log("Schedule not loaded! " + str(e))

    except Exception as e:
        log.error_log("Schedule not loaded! " + str(e))

def bulksmsnigeria_module(phone_number, sender_name, message):
    my_api_token = 'hqAVWyT88lK6es2VjVkA7TlI4Aw1bglAaCqK29Dj8EZ0rm3kShkSFJMxDyge'
    
    if sender_name.strip() = '':
        sender_name = 'AMAS'

    # url = "https://www.bulksmsnigeria.com/api/v1/sms/create?api_token={_api_token}&from={_sender_name}&to={_phone_number}&body={_message}"
    # url = url.format(_api_token = my_api_token, _sender_name = sender_name, _phone_number = phone_number, _message=message)
    
    # response = requests.post(url)


    url = 'http://bulksmsnigeria.test/api/v1/sms/create'
    params = {
    'api_token': 'hqAVWyT88lK6es2VjVkA7TlI4Aw1bglAaCqK29Dj8EZ0rm3kShkSFJMxDyge',
    'to': phone_number,
    'from': 'sender_name',
    'body': message,
    'dnd': 'ut',
    'String': '0',
    }
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

    response = requests.request('POST', url, headers=headers, params=params)  # return json response
    
    return response.json()['data']['status']

def smsclone_module(phone_number, sender_name, message):
        
    if sender_name.strip() = '':
        sender_name = 'AMAS'

    url = 'https://smsclone.com/api/sms/dnd-fallback?username={_username}&password={_password}&sender=@@{_sender}@@&recipient=@@{_recipient}@@&message=@@{_message}@@'
    url = url.format(_username = 'mcchegzy', _password = 'AMAS@smsclone', _sender= 'AMAS', _recipient = '08154410632', _message=message)

    response = requests.post(url) 
    return response.text

def send_sms():
    try:
        conn = sqlite3.connect('db/amas.db')
        # Create cursor
        c = conn.cursor()

        c.execute("SELECT *, oid FROM sms WHERE sent = 0")
        records = c.fetchall()
        
        for record in records: 
            #send SMS module
            status = bulksmsnigeria_module(record[1], 'AMAS', record[0])

            if status == 'success':
                c.execute("""UPDATE sms SET
                    datesent = :_datesent,
                    sent = :_sent

                    WHERE oid = :_oid   
                    """,
                    {
                        'datesent' : datetime.date.today(),
                        'sent' : '1',
                        '_oid': oid
                    }                
                )
            else:
                log.error_log("Couldn't sent with response {0}".format(status))
            
        # Commit Changes
        conn.commit()
        # Close Connection
        conn.close()
        log.error_log("SMS Sent!")

    except IOError as e:
        raise RuntimeError
        
        log.error_log("SMS not sent! " + str(e))
        
    except AttributeError as e:
        raise RuntimeError
        log.error_log("SMS not sent! " + str(e))

    except Exception as e:
        log.error_log("SMS not sent! " + str(e))
