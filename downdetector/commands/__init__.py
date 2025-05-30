from downdetector import bot

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """
    Бот для контроля за состоянием серверов стримингового сервиса.
    Поддерживаемые команды:
    [/ping](/ping) - проверить состояние сервера насильно
    [/subscribe](/subscribe) - подписаться на состояние сервера
    [/unsubscribe](/unsubscribe) - отписаться на состояния сервера
    """)

@bot.message_handler(commands=['hello'])
def hello_user(message):
    bot.reply_to(message, f"👋 Привет, {message.from_user.full_name}!")


import downdetector.commands.subscriptions