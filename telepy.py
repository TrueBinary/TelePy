#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import socket,os,sys
from time import * 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google_images_download import google_images_download

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

mode = os.getenv("mode")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
	def run(updater):
		updater.start_polling()
elif mode == "proud":
	def run(updater):
		PORT = int(os.environ.get("PORT", "8843"))
		HEROKU_APP_NAME = os.environ.get("tele-py")

		updater.start_webhook(listen="0.0.0.0",
							  port=PORT,
							  url_path=TOKEN)
		updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
else:
	logger.error("No MODE specfied")
	sys.exit(1)							  		




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
	updater = Updater(TOKEN)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("get", get, pass_args=True))
	
	updater.start_polling()
	updater.idle()

if __name__== "__main__":
	main()	

