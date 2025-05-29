from downdetector import bot
from downdetector.services.subscription import subscribe, unsubscribe
from telebot import types

channels = ["MediaMTX", "Flask", "GraphQL"]
user_states = {}

@bot.message_handler(commands=['subscribe'])
def subscribe_handler(message):
    user_states[message.chat.id] = "subscribe"
    markup = types.ReplyKeyboardMarkup()
    for channel in channels:
        markup.add(types.KeyboardButton(channel))
    markup.add(types.KeyboardButton("Exit"))
    bot.reply_to(message, 'Выберите на какой сервер подписаться:', reply_markup=markup)

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe_handler(message):
    user_states[message.chat.id] = "unsubscribe"
    markup = types.ReplyKeyboardMarkup()
    for channel in channels:
        markup.add(types.KeyboardButton(channel))
    markup.add(types.KeyboardButton("Exit"))
    bot.reply_to(message, 'Выберите от какого сервера отписаться:', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_reply_keyboard(message):
    if message.text == "Exit":
        bot.reply_to(
            message,
            "Отмена операции",
            reply_markup=types.ReplyKeyboardRemove()
        )
    elif message.text in channels:
        state = user_states.get(message.chat.id)
        if state == "subscribe":
            subscribe(message.text, message.chat.id)
            bot.reply_to(
                message,
                f"Вы подписались на изменения сервера {message.text}",
                reply_markup=types.ReplyKeyboardRemove()
            )
            del user_states[message.chat.id]
        elif state == "unsubscribe":
            unsubscribe(message.text, message.chat.id)
            bot.reply_to(
                message,
                f"Вы отписались от изменений сервера {message.text}",
                reply_markup=types.ReplyKeyboardRemove()
            )
            del user_states[message.chat.id]
    else:
        bot.reply_to(
            message,
            "Не является допустимым значением"
        )

