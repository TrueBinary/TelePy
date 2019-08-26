#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import socket,os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google_images_download import google_images_download

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update):
	update.message.reply_text("Hi Type something to search on the google and back a image of that")

def help(update):
	update.message.reply_text("help")


def get(bot,update,args):
	chat_id= update.message.chat_id
	bot.send_message(chat_id, text= "Use /get something to get some image")
	for i in range(1):
		name = str(i)
		keyword = args[0]
		dic = os.getcwd() + "/downloads/" + name
		response= google_images_download.googleimagesdownload()
		arguments = {"keywords":keyword,"limit":1,"no_directory":True,"prefix":name,"format":"png"}
		paths = response.download(arguments)
		bot.send_photo(chat_id, photo=open(dic,"rb"))


def main():
	updater = Updater("927710630:AAELvBu6JioptN-cZjI_P1F77zn5ugSEcQo")

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("get", get, pass_args=True))
	
	updater.start_polling()
	updater.idle()

if __name__== "__main__":
	main()	

