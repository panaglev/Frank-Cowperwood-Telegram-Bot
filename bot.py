#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10
#FORMAT OF ADDING OPERATION: [char +/-] [value] [comment]
#EXAMPLE: - 24 bus

import sqlite3
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

bot_api = open("apikey.txt", "r")

updater = Updater(f'{bot_api.read().strip()}', use_context=True)

connection = sqlite3.connect("db.db", check_same_thread=False)

cursor = connection.cursor()

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Enter text in here")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("To add transactioin write /add [+/-] [value] [comment]")
    update.message.reply_text("to see only outcUms write /out, to see only inCums write /in")

def add(update: Update, context: CallbackContext, pass_args=True):
    if context.args[0] == "+" or context.args[0] == "-":
        cursor.execute("INSERT INTO trans VALUES (?, ?, ?, ?)", (context.args[0], context.args[1], context.args[2], context.args[3]))
        update.message.reply_text("Added to DataBase")
        connection.commit()
    else:
        update.message.reply_text("Check the char")

def ls(update: Update, context: CallbackContext, pass_args=True):
    for row in cursor.execute("SELECT char, value, comment FROM trans WHERE user_id = (?)", (context.args[0], )):
        update.message.reply_text(row[0] + str(row[1]) + "₽ " + row[2])

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('add', add))
updater.dispatcher.add_handler(CommandHandler('ls', ls))

updater.start_polling()
