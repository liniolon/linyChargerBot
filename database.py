import sqlite3 as db

con = db.connect('charger.db')

cur = con.cursor()

#cur.execute("create table users (id integer primary key autoincrement, firstname text, lastname text, chatid integer, username text, inviteurl text, peopleinvited integer)")
#cur.execute("create table users_channel (id integer primary key autoincrement, chatid integer , username text)")
cur.execute('create table token (id integer primary key autoincrement, token text, chatid integer) ')
print("OK")