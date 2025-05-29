from config import Config
import telebot
from apscheduler.schedulers.background import BackgroundScheduler


config = Config()
bot = telebot.TeleBot(config.TELEGRAM_TOKEN, parse_mode="MARKDOWN")
scheduler = BackgroundScheduler()
import downdetector.commands
import downdetector.background
def start():
    scheduler.start()
    bot.infinity_polling()