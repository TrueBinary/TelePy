#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import socket,os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google_images_download import google_images_download

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update,context):
	update.message.reply_text("Hi!")

def help(update,context):
	update.message.reply_text("help")

def get(bot,update,args):
	chat_id= update.message.chat_id
	for i in range(1):
		name = i
		dic = os.getcwd() + "/downloads" + name
		response= google_images_download.googleimagesdownload()
		keyword = args[0] = socket.gethostbyname(args[0])
		arguments = {"keywords":keyword,"limit":1,"no_directory":True,"print_url":True,"prefix":name,"format":"png"}
		paths = response.download(arguments)
		bot.send_photo(chat_id, photo=open(dic,"rb"))


def error(update,context):
	logger.warning(f"Update {update} caused error {context.error}")

def main():
	updater = Updater("", use_context=True)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("get", get, pass_args=True))

	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()

if __name__== "__main__":
	main()	

