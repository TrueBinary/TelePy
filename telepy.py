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

MODE = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if MODE == "dev":
	def run(updater):
		updater.start_polling()
elif MODE == "proud":
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
	update.message.reply_text("i will help you with images")

def callback_30(bot,job,update):
	bot.send_message(chat_id=update.message.chat_id,text="DO YOU CAN JUST ONLY SEND A MESSAGE EACH 30 SECUNDS BITCH!! STOP SMAPING")


def help(update):
	update.message.reply_text("Use /get to get some random images of google")


def get(bot,update,context):
	chat_id= update.message.chat_id
	print(os.getcwd())
	try:
		sleep(0.6) 
		keyword = "".join(context.args)
		response= google_images_download.googleimagesdownload()
		arguments = {"keywords":keyword,"limit":1,"no_directory":True,"format":"png"}
		paths = response.download(arguments)
		bot.send_message(chat_id, text= "wait for some seconds")
		sleep(0.5)
		os.system("./rename.sh")
		for i in range(0,99):
			dic = os.getcwd() + "/downloads/" + str(i) +".png" 
			bot.send_photo(chat_id, photo=open(dic,"rb"))
			os.remove(f"{dic}")

	except IndexError as e:
		bot.send_message(chat_id=update.message.chat_id,text="Error none arguments")
		print(f"some error we have here dev look at here {e}")
		sys.exit(1)

def main():
	updater = Updater(TOKEN,use_context=True)
	j = updater.job_queue
	j.run_once(callback_30,30)
	anti_spam = CommandHandler("anti_spam",callback_30)
	updater.dispatcher.add_handler(anti_spam)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("get", get, pass_args=True))
	
	updater.start_polling()
	run(updater)

if __name__== "__main__":
	main()	

