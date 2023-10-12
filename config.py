from telebot import types
from models import *
import requests
from io import BytesIO

API_TOKEN = ''

allowed_users = []

db_start()
categories = get_all_name_categories()
button1 = types.KeyboardButton("Заказы")
button2 = types.KeyboardButton("Товары")
button3 = types.KeyboardButton("Профиль")
button4 = types.KeyboardButton("Все товары")
button5 = types.KeyboardButton("Назад")

button6 = types.KeyboardButton("Редактировать профиль")
button7 = types.KeyboardButton("Посмотреть профиль")



button8 = types.KeyboardButton("Имя")
button9 = types.KeyboardButton("Номер телефона")
button10 = types.KeyboardButton("Электронная почта")
button11 = types.KeyboardButton("Следующий товар")
button12 = types.KeyboardButton("Предыдущий товар")
button13 = types.KeyboardButton("Добавить в заказ")
button14 = types.KeyboardButton("Корзина")
button15 = types.KeyboardButton("История заказов")
button16 = types.KeyboardButton("Оформить заказ")
button17 = types.KeyboardButton("Оплатить")
admin_button2 = types.KeyboardButton("Добавить категорию")
admin_button = types.KeyboardButton("Добавить товар")


def mainMenu(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(button1, button2, button3)
    if message.from_user.id in allowed_users:
        markup.add(admin_button, admin_button2)
    return markup


def addMenu():
    markup = types.ReplyKeyboardMarkup()
    markup.add(button4, button5)
    return markup

def profileMenu():
    markup = types.ReplyKeyboardMarkup()
    markup.add(button5, button6, button7)
    return markup


def editMenu():
    markup = types.ReplyKeyboardMarkup()
    markup.add(button8, button9, button10)
    return markup


def productMenu():
    markup = types.ReplyKeyboardMarkup()
    markup.add(button5, button12, button13, button11)
    return markup

def ordersMenu():
    markup = types.ReplyKeyboardMarkup()
    markup.add(button5, button14, button15)
    return markup 


def cartMenu():
    markup = types.ReplyKeyboardMarkup()
    markup.add(button5, button16)
    return markup

def checkoutMenu():
    markup = types.ReplyKeyboardMarkup()
    markup.add(button5, button17)
    return markup