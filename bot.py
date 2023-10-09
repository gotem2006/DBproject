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
    bot.register_next_step_handler(message, suplies_in_category)


def suplies_in_category(message):
    if message.text != "Все товары" and message.text != "Назад":
        category_id = get_categoryID(message.text)
        all_productsInCategory = get_products_from_categoty(category_id)
        for product in all_productsInCategory:
            respones = requests.get(product[4])
            bot.send_photo(message.from_user.id, BytesIO(respones.content))
            bot.send_message(message.from_user.id, f"Название: {product[2]}\nЦена: {product[1]} рублей\nОписание: {product[3]}")
    

@bot.message_handler(func=lambda message: message.text == "Все товары")
def show_all_products(message):
    products = all_product()
    for product in products:
        respones = requests.get(product[4])
        bot.send_photo(message.from_user.id, BytesIO(respones.content))
        bot.send_message(message.from_user.id, f"Название: {product[2]}\nЦена: {product[1]}\nОписание: {product[3]}")
    return


@bot.message_handler(func=lambda message: message.text == "Профиль")
def add_user(message):
    db_start()
    status = get_user_registration_status(message.from_user.id)
    if status == 0:
        bot.send_message(message.from_user.id, "Введите ваше имя:")
        bot.register_next_step_handler(message, load_user_name)
    else:
        markup = profileMenu()
        bot.send_message(message.from_user.id,"Вы профиль уже зарегистрирован!",reply_markup=markup)
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


@bot.message_handler(func=lambda message: message.text == "Заказы" )
def all_orders(message):
    user_orders = get_all_users_orders(message.from_user.id)
    if len(user_orders) <= 0:
        bot.send_message(message.from_user.id, "У вас нету заказов!")
    else:
        for order in user_orders:
            bot.send_message(message.from_user.id, "")



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

@bot.message_handler(func=lambda message: message.text == "Далее")
def next_product(message):
    pass


@bot.message_handler(func=lambda message: message.text == "Добавить в корзину")
def add_to_cart(messsage):
    pass

bot.infinity_polling()