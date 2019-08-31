#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import socket,os
from time import * 
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
	print(os.getcwd())
	for i in range(0,99):
		keyword = args[0]
		response= google_images_download.googleimagesdownload()
		arguments = {"keywords":keyword,"limit":1,"no_directory":True,"format":"png"}
		paths = response.download(arguments)
		bot.send_message(chat_id, text= "wait for some seconds")
		sleep(0.5)
		os.system("./rename.sh")
		dic = os.getcwd() + "/downloads/" + str(i) +".png" 
		bot.send_photo(chat_id, photo=open(dic,"rb"))
		os.remove("~/Área\\ de\\ Trabalho/Scripts/TelePy/downloads/*png*")


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

