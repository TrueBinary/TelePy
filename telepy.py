#lib importantes
#-*- coding: utf-8 -*-

#Copyright (C) 2008 MrTrue <gui19787@gmail.com>
#     This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>


#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import socket,os,sys
from time import * 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, DelayQueue
from google_images_download import google_images_download

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.DEBUG)

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

def start(bot,update):
	chat_id = update.message.chat_id
	msg_id = update.message.message_id
	botwelcome = """Welcome to the pybobot i'll send to you some random images which you want,why do you not try send /get some shit ?"""
	bot.send_message(chat_id=chat_id, text=botwelcome, reply_text=msg_id)

def callback_30(bot,job,update):
	bot.send_message(chat_id=chat_id,text="DO YOU CAN JUST ONLY SEND A MESSAGE EACH 30 SECUNDS BITCH!! STOP SMAPING")


def ajuda(bot,update):
	update.message.reply_text("Use /get to get some random images of google")


def get(bot,update,args,job_queue):
	print(os.getcwd())
	chat_id = update.message.chat_id
	try:
		if len(args) == 1:
			keyword = args[0]
			response= google_images_download.googleimagesdownload()
			arguments = {"keywords":keyword,"limit":1,"no_directory":True,"format":"png","print_urls":True}
			paths = response.download(arguments)
			bot.send_message(chat_id, text= "wait for some seconds")
			sleep(0.7)
			for i in os.listdir("/app/downloads/"):
				nome = str(i)
				dic = os.getcwd() + "/downloads/" + nome 
				bot.send_photo(chat_id, photo=open(dic,"rb"))
				os.remove(f"{dic}")

		elif len(args) == 2:
			keyword = args[0]
			sufkey = args[1]
			response= google_images_download.googleimagesdownload()
			arguments = {"keywords":keyword,"suffix_keywords":sufkey,"limit":1,"no_directory":True,"format":"png","print_urls":True}
			paths = response.download(arguments)
			bot.send_message(chat_id, text= "wait for some seconds")
			sleep(0.7)
			for i in os.listdir("/app/downloads/"):
				nome = str(i)
				dic = os.getcwd() + "/downloads/" + nome 
				bot.send_photo(chat_id, photo=open(dic,"rb"))
				os.remove(f"{dic}")
		else:
			prekey = args[0]
			keyword = args[1]
			sufkey = args[2]
			response= google_images_download.googleimagesdownload()
			arguments = {"keywords":keyword,"suffix_keywords":sufkey,"prefix_keywords":prekey,"limit":1,"no_directory":True,"format":"png","print_urls":True}
			paths = response.download(arguments)
			bot.send_message(chat_id, text= "wait for some seconds")
			sleep(0.7)
			for i in os.listdir("/app/downloads/"):
				nome = str(i)
				dic = os.getcwd() + "/downloads/" + nome 
				bot.send_photo(chat_id, photo=open(dic,"rb"))
				os.remove(f"{dic}")

	except IndexError as e:
		bot.send_message(chat_id=chat_id,text="Error none arguments")
		print(f"some error we have here dev look at here {e}")
		

def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help", ajuda))
	dp.add_handler(CommandHandler("get", get, pass_args=True,pass_job_queue=True))
	j = dp.job_queue
	job_minute = j.run_once(get,25)
	
	updater.start_polling()
	run(updater)

if __name__== "__main__":
	main()	

"""/TODO add new feature google reverse image """