import sqlite3

connetion = sqlite3.connect('Products.db')
cursor = connetion.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
);
''')


def initiate_db(title_, description_, price_):
    cursor.execute("INSERT INTO Users (title, description, price) VALUES (?, ?, ?)", (title_, description_, price_))
    connetion.commit()


connetion.commit()
connetion.close()
