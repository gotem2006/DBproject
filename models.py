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
                registration_status INTEGER,\
                position INTEGER)")
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
                delivery_adress TEXT,\
                user_id INTEGER,\
                FOREIGN KEY(user_id) REFERENCES user(user_id))")
    db.commit()


# Заказы
def set_delivary_adress(user_id, deliavary_adress):
    cur.execute("UPDATE orders SET delivery_adress = ? WHERE user_id = ? AND status = ?",(deliavary_adress, user_id, "1",))
    db.commit()

def update_status(user_id, status_set, status_setted):
    cur.execute("UPDATE orders SET status= ? WHERE user_id =? AND status = ?", (status_set, user_id, status_setted,))
    db.commit()

def get_all_users_orders(user_id):
    user_orders = cur.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,)).fetchall()
    return user_orders

def get_orders_history(user_id, status):
    history = cur.execute("SELECT * FROM orders WHERE user_id = ? AND status = ?",(user_id, status,)).fetchall()
    return history

def add_order(user_id, suplies, total_price):
    order = cur.execute("SELECT 1 FROM orders WHERE user_id = ?",(user_id,)).fetchone()
    if not order:
        cur.execute("INSERT INTO orders (suplies, user_id, totalPrice, status) VALUES (?, ?, ?, ?)",(suplies, user_id, total_price, "1",))
    else:
        cur.execute("UPDATE orders SET totalPrice = ?, suplies = ? WHERE user_id = ?",(total_price, suplies, user_id,))
    db.commit()

def get_order(user_id, status):
    order = cur.execute("SELECT * FROM orders WHERE user_id =? AND status = ?",(user_id, status,)).fetchone()
    return order
def get_suplies_from_order(user_id):
    suplies = cur.execute("SELECT suplies FROM orders WHERE user_id =?",(user_id,)).fetchone()
    if not suplies:
        return ""
    return suplies[0]

def get_total_price(user_id):
    total_price = cur.execute("SELECT totalPrice FROM orders WHERE user_id = ?", (user_id,)).fetchone()
    if not total_price:
        total_price = 0
        return total_price
    return total_price[0]

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

def get_all_name_categories():
    names = []
    for name in cur.execute("SELECT name FROM categories").fetchall():
        names.append(name[0])
    return names

def get_name_of_category(category_id):
    category_name = cur.execute("SELECT name FROM categories WHERE category_id = ?", (category_id,)).fetchall()
    return category_name

# Пользователь
def create_profile(telegram_id):
    user = cur.execute("SELECT 1 FROM user WHERE telegram_id = ?", (telegram_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO user (telegram_id, name, phonenumber, email, registration_status, position) VALUES(?, ?, ?, ?, ?, ?)", (telegram_id, '', '', '', 0, 0))
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

def change_position(user_id, position):
    cur.execute("UPDATE user SET position = ? WHERE telegram_id = ?",(position,user_id,))
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

def get_product_price(product_id):
    price = cur.execute("SELECT price FROM suplies WHERE suplies_id =?",(product_id,)).fetchone()
    return price[0]

def get_product(product_id):
    product = cur.execute("SELECT * FROM SUPLIES WHERE suplies_id =?",(product_id,)).fetchone()
    return product