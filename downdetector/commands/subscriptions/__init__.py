from downdetector import bot
from downdetector.services.subscription import subscribe, unsubscribe
import downdetector.background as bg
from telebot import types

channels = ["MediaMTX", "Flask", "GraphQL"]

@bot.message_handler(commands=['ping'])
def unsubscribe_handler(message):
    markup = types.InlineKeyboardMarkup()
    for channel in channels:
        markup.add(types.InlineKeyboardButton(channel, callback_data=f'ping_{channel}'))
    bot.reply_to(message, 'Выберите состояние какого сервера проверить:', reply_markup=markup)

@bot.message_handler(commands=['subscribe'])
def subscribe_handler(message):
    markup = types.InlineKeyboardMarkup()
    for channel in channels:
        markup.add(types.InlineKeyboardButton(channel, callback_data=f'subscribe_{channel}'))
    bot.reply_to(message, 'Выберите на какой сервер подписаться:', reply_markup=markup)

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe_handler(message):
    markup = types.InlineKeyboardMarkup()
    for channel in channels:
        markup.add(types.InlineKeyboardButton(channel, callback_data=f'unsubscribe_{channel}'))
    bot.reply_to(message, 'Выберите от какого сервера отписаться:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'ping_MediaMTX')
def ping_media_mtx(call):
    message = call.message
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "❗[[MediaMTX]]: ✅ Сервер в рабочем состоянии!"
        if bg.ping_media_mtx() else
        "❗[[MediaMTX]]: ❌ Сервер недоступен!"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'subscribe_MediaMTX')
def subscribe_media_mtx(call):
    message = call.message
    chat_id = message.chat.id
    subscribe("MediaMTX", chat_id)
    bot.send_message(chat_id, "ℹ️[[MediaMTX]]: Вы подписались на изменения сервера!")

@bot.callback_query_handler(func=lambda call: call.data == 'unsubscribe_MediaMTX')
def unsubscribe_media_mtx(call):
    message = call.message
    chat_id = message.chat.id
    unsubscribe("MediaMTX", message.chat.id)
    bot.send_message(chat_id, "ℹ️[[MediaMTX]]: Вы отписались от изменений сервера MediaMTX")


@bot.callback_query_handler(func=lambda call: call.data == 'ping_Flask')
def ping_flask(call):
    message = call.message
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "❗[[Flask]]: ✅ Сервер в рабочем состоянии!"
        if bg.ping_flask() else
        "❗[[Flask]]: ❌ Сервер недоступен!"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'subscribe_Flask')
def subscribe_flask(call):
    message = call.message
    chat_id = message.chat.id
    subscribe("Flask", chat_id)
    bot.send_message(chat_id, "ℹ️[[Flask]]: Вы подписались на изменения сервера Flask")

@bot.callback_query_handler(func=lambda call: call.data == 'unsubscribe_Flask')
def unsubscribe_flask(call):
    message = call.message
    chat_id = message.chat.id
    unsubscribe("Flask", message.chat.id)
    bot.send_message(chat_id, "ℹ️[[Flask]]: Вы отписались от изменений сервера Flask")


@bot.callback_query_handler(func=lambda call: call.data == 'ping_GraphQL')
def ping_graph_ql(call):
    message = call.message
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "❗[[GraphQL]]: ✅ Сервер в рабочем состоянии!"
        if bg.ping_graphql() else
        "❗[[GraphQL]]: ❌ Сервер недоступен!"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'subscribe_GraphQL')
def subscribe_graph_ql(call):
    message = call.message
    chat_id = message.chat.id
    subscribe("GraphQL", chat_id)
    bot.send_message(chat_id, "ℹ️[[GraphQL]]: Вы подписались на изменения сервера GraphQL")

@bot.callback_query_handler(func=lambda call: call.data == 'unsubscribe_GraphQL')
def unsubscribe_graph_ql(call):
    message = call.message
    chat_id = message.chat.id
    unsubscribe("GraphQL", message.chat.id)
    bot.send_message(chat_id, "ℹ️[[GraphQL]]: Вы отписались от изменений сервера GraphQL")

