import telebot
from telebot import types
import test

bot = telebot.TeleBot("TOKEN_BOT")
message_list = [" ", " "]
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Остатки")
    btn2 = types.KeyboardButton("Отгрузки")
    btn3 = types.KeyboardButton("Поступления")
    btn4 = types.KeyboardButton("Внести поступление/отгрузку")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text="Wassup, {0.first_name}! Что бы вы хотели узнать?".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Остатки":
        message_list.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Общий остаток в рублях")
        btn2 = types.KeyboardButton("Остаток определенного товара")
        btn3 = types.KeyboardButton("Остаток контроллеров")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id, text="Выберите вариант", reply_markup=markup)
    elif message.text == "Отгрузки":
        message_list.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        week = types.KeyboardButton("За неделю")
        month = types.KeyboardButton("За месяц")
        markup.add(week, month)
        bot.send_message(message.chat.id, text="За какой промежуток вывести отгрузки?", reply_markup=markup)
    elif message.text == "Поступления":
        message_list.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        week = types.KeyboardButton("За неделю")
        month = types.KeyboardButton("За месяц")
        markup.add(week, month)
        bot.send_message(message.chat.id, text="За какой промежуток вывести поступления?", reply_markup=markup)
    elif message.text == "За неделю":
        message_list.append(message.text)
        if message_list[-2] == "Поступления":
            print(message_list[-2])
            delivery = test.delivery(0)
            bot.send_message(message.chat.id, f'Поступления:\n{ delivery }')
        elif message_list[-2] == "Отгрузки":
            shipments = test.shipments(0)
            bot.send_message(message.chat.id, f'Отгрузки:\n{ shipments }')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        bot.send_message(message.chat.id, text="Вернитесь в главное меню", reply_markup=markup)
    elif message.text == "За месяц":
        message_list.append(message.text)
        if message_list[-2] == "Поступления":
            delivery = test.delivery(1)
            bot.send_message(message.chat.id, f'Поступления:\n{ delivery }')
        elif message_list[-2] == "Отгрузки":
            shipments = test.shipments(1)
            bot.send_message(message.chat.id, f'Отгрузки:\n{ shipments }')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        bot.send_message(message.chat.id, text="Вернитесь в главное меню", reply_markup=markup)
    elif message.text == "Поступление":
        message_list.append(message.text)
        bot.send_message(message.chat.id, "Введите артикул поступившего товара")
    elif message.text == "Отгрузка":
        message_list.append(message.text)
        bot.send_message(message.chat.id, "Введите артикул отгруженного товара")
    elif message.text == "Общий остаток в рублях":
        message_list.append(message.text)
        total_rest = test.cash_rest()
        bot.send_message(message.chat.id, f'Остаток товара на складе { total_rest } рублей')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
    elif message.text == "Остаток определенного товара":
        message_list.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        yes = types.KeyboardButton("Да")
        no = types.KeyboardButton("Нет")
        markup.add(yes, no)
        bot.send_message(message.chat.id, text="Хотите посмотреть список артиклей?", reply_markup=markup)
    elif message.text == "Да" and message_list[-1] == "Остаток определенного товара":
        bot.send_message(message.chat.id, test.article())
        bot.send_message(message.chat.id, "Введите артикул товара")
    elif message.text == "Нет" and message_list[-1] == "Остаток определенного товара":
        bot.send_message(message.chat.id, "Введите артикул товара")
    elif message.text == "Остаток контроллеров":
        message_list.append(message.text)
        cont_rest = test.rest_of_controllers()
        bot.send_message(message.chat.id, f'Остаток контроллеров на складе:\n { cont_rest }')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
    elif message.text == "Вернуться в главное меню":
        message_list.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        message_list.clear()
        message_list.append(' ')
        message_list.append(' ')
        btn1 = types.KeyboardButton("Остатки")
        btn2 = types.KeyboardButton("Отгрузки")
        btn3 = types.KeyboardButton("Поступления")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    elif message.text == "Ввести артикул заново":
        message_list.append(message.text)
        bot.send_message(message.chat.id, "Введите артикул товара")
    else:
        if message_list[-1] == "Остаток определенного товара" or message_list[-1] == "Ввести артикул заново":
            try:
                rest = test.rest_of_good(message.text)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                again = types.KeyboardButton("Ввести артикул заново")
                back = types.KeyboardButton("Вернуться в главное меню")
                markup.add(again, back)
                bot.send_message(message.chat.id, f'{rest}', reply_markup=markup)
            except ValueError:
                bot.send_message(message.chat.id, text="Артикул введен неверно")
        elif message_list[-1] == "Поступление" or message_list[-1] == "Отгрузка" or message_list[-1] == "Артикул введен неверно, введите заново":
            article = message.text
            global name 
            name = test.is_correct_article(article)
            if name == 0:
                bot.send_message(message.chat.id, text="Артикул введен неверно, введите заново")
                message_list.append("Артикул введен неверно, введите заново")
            else:
                message_list.append("Введите количество")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("Вернуться в главное меню")
                markup.add(back)
                bot.send_message(message.chat.id, "Введите количество", reply_markup=markup)
        elif message_list[-1] == "Введите количество" or message_list[-1] == "Количество введено некорректно, введите заново":
            try:
                amount = message.text
                if message_list[-2] == "Поступление":
                    test.post_new(name, "delivery", amount)
                elif message_list[-2] == "Отгрузка":
                    test.post_new(name, "shipment", amount)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("Вернуться в главное меню")
                markup.add(back)
                bot.send_message(message.chat.id, "Данные внесены", reply_markup=markup)
            except ValueError:
                message_list.append("Количество введено некорректно, введите заново")
                bot.send_message(message.chat.id, text="Количество введено некорректно, введите заново")
        else:
            bot.send_message(message.chat.id, text="Такой команды нет")

bot.polling(none_stop=True)