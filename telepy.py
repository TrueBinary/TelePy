#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import socket,os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google_images_download import google_images_download

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update,context):
	update.message.reply_text("Hi Type something to search on the google and back a image of that")

def help(update,context):
	update.message.reply_text("help")


def get(bot,update,args):
	chat_id= update.message.chat_id
	bot.send_message(chat_id, text= "Use /get something to get some image")
	for i in range(1):
		name = str(i)
		dic = os.getcwd() + "/downloads" + name
		response= google_images_download.googleimagesdownload()
		arguments = {"keywords":args[0],"limit":1,"no_directory":True,"print_url":True,"prefix":name,"format":"png"}
		paths = response.download(arguments)
		bot.send_photo(chat_id, photo=open(dic,"rb"))


def error(update,context):
	logger.warning(f"Update {update} caused error {context.error}")

def main():
	updater = Updater("",use_context=True)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("get", get, pass_args=True))

	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()

if __name__== "__main__":
	main()	

