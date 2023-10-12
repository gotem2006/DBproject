import telebot
from telebot import types
from models import *
from config import *
import requests
from io import BytesIO


bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'],content_types=['text','photo'])
def start(message):
    db_start()
    markup = mainMenu(message)
    bot.send_message(message.from_user.id, "Рады вас приветствовать в нашем магазине!", reply_markup=markup)
    create_profile(message.from_user.id)



@bot.message_handler(func=lambda message: message.text == "Добавить категорию")
def add_category(message):
    bot.send_message(message.from_user.id, "Введите название категории:")
    bot.register_next_step_handler(message, load_category_name)

def load_category_name(message):
    category_name = message.text
    create_category(category_name)
    bot.send_message(message.from_user.id, "Категория успешно создана!")



@bot.message_handler(func=lambda message: message.text == "Добавить товар")
def add_product(message):
    db_start()
    bot.send_message(message.from_user.id,"Введите название товара:")
    bot.register_next_step_handler(message, load_product_name)

def load_product_name(message):
    product_name = message.text
    bot.send_message(message.from_user.id,"Введите цену товара:")
    bot.register_next_step_handler(message, load_product_price, product_name)


def load_product_price(message, product_name):
    product_price = message.text
    bot.send_message(message.from_user.id, "Введите описание товара:")
    bot.register_next_step_handler(message, load_product_description, product_name, product_price)

def load_product_description(message, product_name, product_price):
    product_description = message.text
    categories = get_all_categories()
    markup2 = types.ReplyKeyboardMarkup()
    for category in categories:
        markup2.add(types.KeyboardButton(f"{category[1]}"))
    bot.send_message(message.from_user.id, "Введите категорию товара:", reply_markup=markup2)
    bot.register_next_step_handler(message, load_product_category, product_name, product_price, product_description)


def load_product_category(message, product_name, product_price, product_description):
    product_category = get_categoryID(message.text)
    bot.send_message(message.from_user.id, "Выберите изображение товара:")
    bot.register_next_step_handler(message, load_product_photo, product_name, product_price, product_description, product_category)

def load_product_photo(message, product_name, product_price, product_description, product_category):
    product_photos = bot.get_file_url(message.photo[-1].file_id)
    create_product(product_name, product_price, product_description, product_category, product_photos)
    bot.send_message(message.from_user.id, "Товвар добавлен")



@bot.message_handler(func=lambda message: message.text == "Товары")
def all_products(message):
    db_start()
    categories = get_all_categories()
    markup = addMenu()
    
    for category in categories:
        markup.add(types.KeyboardButton(f"{category[1]}"))
    bot.send_message(message.from_user.id, "Выберите категорию товара", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in categories)
def suplies_in_category(message):
    category_id = get_categoryID(message.text)
    all_productsInCategory = get_products_from_categoty(category_id)
    for product in all_productsInCategory:
        respones = requests.get(product[4])
        bot.send_photo(message.from_user.id, BytesIO(respones.content))
        bot.send_message(message.from_user.id, f"Название: {product[2]}\nЦена: {product[1]} рублей\nОписание: {product[3]}")
    

@bot.message_handler(func=lambda message: message.text == "Все товары")
def show_all_products(message):
    products = all_product()
    user_position = get_user_info(message.from_user.id)[6]
    if user_position < len(products):
        markup = productMenu()
        product = products[user_position]
        respones = requests.get(product[4])
        bot.send_photo(message.from_user.id, BytesIO(respones.content))
        bot.send_message(message.from_user.id, f"Название: {product[2]}\nЦена: {product[1]}\nОписание: {product[3]}", reply_markup=markup)
        user_position += 1
        if user_position >= len(products):
            user_position = 0
        change_position(message.from_user.id, user_position)
        
    
    
@bot.message_handler(func=lambda message: message.text == "Предыдущий товар")
def previous_product(message):
    products = all_product()
    user_position = get_user_info(message.from_user.id)[6]
    if user_position < len(products):
        markup = productMenu()
        product = products[user_position]
        respones = requests.get(product[4])
        bot.send_photo(message.from_user.id, BytesIO(respones.content))
        bot.send_message(message.from_user.id, f"Название: {product[2]}\nЦена: {product[1]}\nОписание: {product[3]}", reply_markup=markup)
        user_position -=  1
        change_position(message.from_user.id, user_position)

    else:
        user_position = len(all_product())-1
        change_position(message.from_user.id, user_position)
        markup = productMenu()
        product = products[user_position]
        respones = requests.get(product[4])
        bot.send_photo(message.from_user.id, BytesIO(respones.content))
        bot.send_message(message.from_user.id, f"Название: {product[2]}\nЦена: {product[1]}\nОписание: {product[3]}", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Следующий товар")
def next_product(message):
    products = all_product()
    user_position = get_user_info(message.from_user.id)[6]
    if user_position < len(products):
        markup = productMenu()
        product = products[user_position]
        respones = requests.get(product[4])
        bot.send_photo(message.from_user.id, BytesIO(respones.content))
        bot.send_message(message.from_user.id, f"Название: {product[2]}\nЦена: {product[1]}\nОписание: {product[3]}", reply_markup=markup)
        user_position += 1
        if user_position >= len(products):
            user_position = 0
        change_position(message.from_user.id, user_position)

    
@bot.message_handler(func=lambda message: message.text == "Профиль")
def add_user(message):
    db_start()
    status = get_user_info(message.from_user.id)[5]
    if status == 0:
        bot.send_message(message.from_user.id, "Введите ваше имя:")
        bot.register_next_step_handler(message, load_user_name)
    else:
        markup = profileMenu()
        bot.send_message(message.from_user.id,f"Вы профиль уже зарегистрирован!{status}",reply_markup=markup)
        return

def load_user_name(message):
    user_name = message.text
    bot.send_message(message.from_user.id, "Введите ваш номер телефона:")
    bot.register_next_step_handler(message, load_phonenumber, user_name)

def load_phonenumber(message, user_name):
    user_phonenumber = message.text
    bot.send_message(message.from_user.id, "Введите ваш email:")
    bot.register_next_step_handler(message, load_email, user_name, user_phonenumber )

def load_email(message, user_name, user_phonenumber):
    user_email = message.text
    edit_profile(message.from_user.id, user_name, user_phonenumber, user_email, 1)
    bot.send_message(message.from_user.id, "Ваш профиль успешно создан!")

@bot.message_handler(func=lambda message: message.text == "Назад")
def bact_to_menu(message):
    markup = mainMenu(message)
    bot.send_message(message.from_user.id, "Вы вернулись в главное меню", reply_markup= markup)


@bot.message_handler(func=lambda message: message.text == "Редактировать профиль")
def edit_profile_info(message):
    markup = editMenu()
    bot.send_message(message.from_user.id, "Что вы хотите изменить?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Имя")
def edit_name(message):
    bot.send_message(message.from_user.id, "Введите новое имя:")
    bot.register_next_step_handler(message, load_new_user_name)

def load_new_user_name(message):
    change_name(message.text, message.from_user.id)
    bot.send_message(message.from_user.id, "Вы изменили имя!")

@bot.message_handler(func=lambda message: message.text == "Номер телефона")
def edit_phonenumber(message):
    bot.send_message(message.from_user.id, "Введите новой номер телефона:")
    bot.register_next_step_handler(message, load_new_user_phonenumber)

def load_new_user_phonenumber(message):
    change_phonenumber(message.text, message.from_user.id)
    bot.send_message(message.from_user.id, "Вы изменили номер телефона!")



@bot.message_handler(func=lambda message: message.text == "Электронная почта")
def edit_email(message):
    bot.send_message(message.from_user.id, "Введите новую электронную почту:")
    bot.register_next_step_handler(message, load_new_email)

def load_new_email(message):
    change_email(message.text, message.from_user.id)
    bot.send_message(message.from_user.id, "Вы изменили свою электронную почту!")



@bot.message_handler(func=lambda message: message.text == "Посмотреть профиль")
def show_profile(message):
    user = get_user_info(message.from_user.id)
    bot.send_message(message.from_user.id, f"Ваше имя: {user[2]}\nВаш номер телефона: {user[3]}\nВаша электронная почта: {user[4]}")


@bot.message_handler(func=lambda message: message.text == "Добавить в заказ")
def add_to_cart(message):
    total_price = get_total_price(message.from_user.id)
    user_position = get_user_info(message.from_user.id)[6] + 1
    total_price += get_product_price(user_position)
    suplies = get_suplies_from_order(message.from_user.id)
    if suplies == "":
        suplies += f"{user_position}"
    else:
        suplies += f"{ user_position}"
    add_order(message.from_user.id, suplies, total_price)


@bot.message_handler(func=lambda message: message.text == "Заказы")
def orders(message):
    markup= ordersMenu()
    bot.send_message(message.from_user.id, "Какой раздел вамнужен?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Корзина")
def display_orders(message):
    order = get_order(message.from_user.id, "1")
    if not order:
        bot.send_message(message.from_user.id, "В корзине нет товаров!")
        return
    suplies_id = order[2].split(" ")
    suplies = []
    for item in range(len(suplies_id)):
        suplies.append(get_product(int(suplies_id[item])))

    count = 1
    markup = cartMenu()
    bot.send_message(message.from_user.id, "Ваша корзина:")
    for product in suplies:
        respones = requests.get(product[4])
        bot.send_photo(message.from_user.id, BytesIO(respones.content), caption=f'Товар №{count}\nНазвание: {product[2]}\nОписание: {product[3]}\nСтоимлсть: {product[1]}')
        count += 1 
    bot.send_message(message.from_user.id, f"Итоговая стоимость заказа: {order[3]}", reply_markup=markup)




@bot.message_handler(func=lambda message: message.text == "История заказов")
def show_history(message):
    orders_history = get_orders_history(message.from_user.id, "2")
    if not orders_history:
        bot.send_message(message.from_user.id, "У вас нету заказов!")
        return
    count_order = 1
    count_product = 1
    for order in orders_history:
        suplies_id = order[2].split(" ")
        suplies = [get_product(int(item)) for item in suplies_id]
        bot.send_message(message.from_user.id, f"Заказ №{count_order}")
        for suply in suplies:
            respones = requests.get(suply[4])
            bot.send_photo(message.from_user.id, BytesIO(respones.content), f'Товар №{count_product}\nНазвание: {suply[2]}\nОписание: {suply[3]}\nСтоимлсть: {suply[1]}')
            count_product += 1
        bot.send_message(message.from_user.id, f"Тоговая стоимость заказа: {order[3]}")
        count_product = 1
        count_order += 1


@bot.message_handler(func=lambda message: message.text == "Оформить заказ")
def checkout(message):
    markup = checkoutMenu()
    bot.send_message(message.from_user.id, "Введите адресс доставки:", reply_markup=markup)
    bot.register_next_step_handler(message, load_adress)

def load_adress(message):
    adress = message.text
    set_delivary_adress(message.from_user.id, adress)

@bot.message_handler(func=lambda message: message.text == "Оплатить")
def pay(message):
    update_status(message.from_user.id, "2", "1")
    bot.send_message(message.from_user.id, "Ваш заказ передан в обработку!")

bot.infinity_polling()