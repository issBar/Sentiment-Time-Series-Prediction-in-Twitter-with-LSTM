# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error
 
db_file="./sqlite/db/Tweet_sqlite.db"

 
def create_connection(user,consumer_key,consumer_secret,access_token,access_token_secret):
    """ create a database connection to a SQLite database """
    print("user=",user)
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        cursor=conn.cursor()
        
        #creating table if now exist
        create_table(conn)

        
        #inserting
        cursor.execute('''INSERT INTO authentications(consumer_key,consumer_secret,access_token,access_token_secret,user) VALUES(?,?,?,?,?)''',(consumer_key,consumer_secret,access_token,access_token_secret,user))    
        conn.commit()
        print("succsses to insert database/n")

        
    except Error as e:
        print(e)
        
    finally:
        conn.close()
 
def create_table(conn):
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE if not exists authentications (consumer_key,consumer_secret,access_token,access_token_secret,user)''')
    conn.commit()
    

def get_authentication():
    
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        cursor=conn.cursor()
        cursor=cursor.execute('''SELECT consumer_key,consumer_secret,access_token,access_token_secret FROM authentications''') 
        conn.commit()
        
        for c in cursor:
            consumer_key=c[0]
            consumer_secret=c[1]
            access_token=c[2]
            access_token_secret=c[3]
           
            
        return consumer_key,consumer_secret,access_token,access_token_secret
            

    except Error as e:
        print(e)
    finally:
        conn.close()
        
def get_user_name():
    try:
        print("getting user\n")
        user=''
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        cursor=conn.cursor()
        cursor=cursor.execute('''SELECT user FROM authentications''') 
        conn.commit()
        for c in cursor:
            user=c[0]
            
        return user
    
    
    except Error as e:
        print(e)
        return user
    finally:
        conn.close()
        
def dropTable():
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        cursor=conn.cursor()
        cursor=cursor.execute('''DROP TABLE authentications''')
        print("Drop Table\n")
        conn.commit()

        
    except Error as e:
           print(e)
           
    finally:
        conn.close()
    
consumer_key = 'i5UW3ELVfZMBo7v9QfJ5bBK4q'
consumer_secret = 'PzNZLrr8zdvEi3MkHv43mkA6GmgwP8g6J12eDAsfU1HiYpGtZ7'
access_token = '469641234-wAc1uMHBENJwI5S0SUFdED63dMlWwTTTdOVHIrOL'
access_token_secret = '3DSGRzcuFEnRIPzIQaRn17e2xXBARKh1fTlis1H1tGHz5'
user='yaron'

#dropTable()

#create_connection(user,consumer_key,consumer_secret,access_token,access_token_secret)
#get_user_name()

#get_authentication()
