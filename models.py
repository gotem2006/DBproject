import sqlite3 as sq

def db_start():
    global db, cur
    db = sq.connect('database.sql', check_same_thread=False)
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS categories(\
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                name TEXT)")
    db.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS user(\
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                telegram_id TEXT,\
                 name TEXT,\
                phonenumber TEXT,\
                email TEXT,\
                registration_status INTEGER)")
    db.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS suplies(\
                suplies_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                 price FLOAT,\
                 name TEXT,\
                 description TEXT,\
                 photos TEXT,\
                category_id INTEGER,\
                FOREIGN KEY(category_id) REFERENCES categories(category_id))")
    db.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS orders(\
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                status TEXT,\
                suplies TEXT,\
                totalPrice FLOAT,\
                user_id INTEGER,\
                FOREIGN KEY(user_id) REFERENCES user(user_id))")
    db.commit()




# Заказы
def get_all_users_orders(user_id):
    user_orders = cur.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,)).fetchall()
    return user_orders

def add_order(user_id, suply_id):
    cur.execute("INSERT into orders (suplies, user_id) VALUES (?, ?)",(suply_id, user_id,))  # ??????????
    db.commit()



# Категории
def create_category(name):
    cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    db.commit()

def get_all_categories():
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    return categories


def get_categoryID(name):
    category = cur.execute("SELECT category_id FROM categories WHERE name = ?", (name,)).fetchone()
    return category[0]

def get_products_from_categoty(category_id):
    products_in_category = cur.execute("SELECT * FROM suplies WHERE category_id = ?", (category_id,)).fetchall()
    return products_in_category


def get_name_of_category(category_id):
    category_name = cur.execute("SELECT name FROM categories WHERE category_id = ?", (category_id,)).fetchall()
    return category_name




# Пользователь
def create_profile(telegram_id):
    user = cur.execute("SELECT 1 FROM user WHERE telegram_id = ?", (telegram_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO user (telegram_id, name, phonenumber, email, registration_status) VALUES(?, ?, ?, ?, ?)", (telegram_id, '', '', '', 0))
        db.commit()

def create_product(name, price, description, category, photos):
    cur.execute("INSERT INTO suplies (price, name, description, category_id, photos) VALUES (?, ?, ?, ?, ?)",
                (price, name, description, category, photos))
    db.commit()


def edit_profile(telegram_id, user_name, user_phonenumber, user_email, user_registration_status):
    cur.execute("UPDATE user SET name = ?, phonenumber  = ?, email = ?, registration_status = ? WHERE telegram_id = ?", (user_name, user_phonenumber, user_email, user_registration_status, telegram_id))
    db.commit()

    
def all_product():
    cur.execute("SELECT * FROM suplies")
    products = cur.fetchall()
    return products


def change_name(user_name, user_id):
    cur.execute("UPDATE user SET name = ? WHERE telegram_id = ?",(user_name, user_id,))
    db.commit()


def get_user_info(user_id):
    user = cur.execute("SELECT * FROM user WHERE telegram_id = ?", (user_id,)).fetchone()
    return user

def change_phonenumber(user_phonenumber, user_id):
    cur.execute("UPDATE user SET phonenumber = ? WHERE telegram_id = ?",(user_phonenumber, user_id,))
    db.commit()


def change_email(user_email, user_id):
    cur.execute("UPDATE user SET email = ? WHERE telegram_id = ?",(user_email, user_id,))
    db.commit()