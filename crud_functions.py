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
    check_initiate = cursor.execute('SELECT * FROM Users WHERE id == ?', (title_,))
    if check_initiate.fetchone() is None:
        cursor.execute("INSERT INTO Users (title, description, price) VALUES (?, ?, ?)",
                   (f'Продукт:{title_}', f'Название:{description_}', price_))
        connetion.commit()
    return f'Название: Product {title_} | Описание: описание {description_} | Цена: {price_}'



connetion.commit()
# connetion.close()
