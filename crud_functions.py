import sqlite3


def initiate_db():
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

    connetion.commit()


def get_all_products():
    initiate_db()
    connetion = sqlite3.connect('Products.db')
    cursor = connetion.cursor()
    for i in range(1, 5):
        title_ = f'Продукт{i}'
        description_ = f'Описание{i}'
        price_ = i * 100
        check_price = cursor.execute('SELECT id FROM Users WHERE title = ?', (title_,))
        if check_price.fetchone() is None:
            cursor.execute("INSERT INTO Users (title, description, price) VALUES (?, ?, ?)",
                           (f'{title_}', f'{description_}', f'{price_}'))
    price_list = cursor.execute('SELECT * FROM Users')
    message = []
    for user in price_list:
        message.append(f'Название: {user[1]} | Описание: {user[2]} | Стоимость: {user[3]} \n')
    connetion.commit()
    return message




# connetion.commit()
# connetion.close()
