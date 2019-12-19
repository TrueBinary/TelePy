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
import configparser
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import time, threading,queue
import logging
import socket,os,sys
from time import * 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, DelayQueue
from telegram.ext.dispatcher import run_async
from google_images_download import google_images_download

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.DEBUG)

logger = logging.getLogger(__name__)
MODE = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if MODE == "dev":
	def run(updater):
		updater.start_polling()
		updater.idle()
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

def ajuda(bot,update):
	update.message.reply_text("Use /get to get some random images of google")

def crawler(bot,update):
	

	class Reddit(scrapy.Spider):
		chat_id = "@FreeeGamesonSteam"
		name = "reddit"
		subreddit = "https://www.reddit.com/r/FreeGamesOnSteam/"

		def parse(self,response):
			for thing in response.css("div.thing"):
				upvotes = int(thing.css("::attr(data-score)").extratct_first())
				if upvotes >= 1:
					queue.put(
						json.dumps({
							"subreddit": response.request.url.rsplit("/", 2)[1].encode("utf8"),
							"title": str(thing.css("p.title a.title::text").extratct_first().encode("utf8")),
							"upvotes":upvotes,
							"thread_link":response.urljoin(
								thing.css("p.title a.title::attr(href)").extratct_first().encode("utf8")),
							}))
			response.css("div.quote")
			for href in response.css("span.next-button a::attr(href)"):
				yield response.follow(href,self.parse)

	queue = queue.queue()

	send_thread = Result(bot,chat_id,queue)
	send_thread.start()					

	url = []
	for sr in subreddit.split(";"):
		urls.append("https://www.reddit.com/r/" + sr)

	process = CrawlerProcess({"FEED_EXPORT_ENCODING": "utf-8", "LOG_ENABLE": False})
	spider = RedditSpider
	spider.start_urls = urls
	process.crawl(spider)
	process.start()

	send_thread.stop = True
	send_thread.join()

class Result(threading.Thread):


	def __init__(self,bot,chat_id,q):
		self.bot = bot
		self.chat_id = chat_id
		self.queue = q
		self.stop = False
		threading.Thread.__init__(self)
	def run(self):
		while True:

			time.sleep(0.1)
			if not self.queue.empty():
				r = self.queue.get()
				result = json.loads(r)
				text = '<b>' + str(result['title'].encode('utf-8')) + '</b>\n'
				text += '<b>Subreddit:</b> ' + str(result['subreddit'].encode('utf-8')) + '\n'
				text += '<b>Up Votes:</b> ' + str(result['upvotes']) + '\n'
				text += '<b>Thread Link:</b> \n' + str(result['thread_link'].encode('utf-8')) + '\n'	

				try:
					self.bot.send_message(parse_mode="HTML", chat_id=self.chat_id, text=text)
				except Exception as e:
					print(f"error {e}")
			else:
				if self.stop:
					time.sleep(0.2)
					try:
						self.bot.send_message(parse_mode="HTML",chat_id=self.chat_id, text=text)
					except Exception as e:
						print(f"Error {e}")

				time.sleep(1)				


def info(bot,update):
	info_text = """
<b>Hi i'm bot of MrTrue,i was created to help you find some imagens on the google</b>
<b>Developer: </b> <a href="https://t.me/Mr_True">MrTrue</a>
<b>Code: </b> <a href="https://github.com/TrueBinary/TelePy">Github</a>
	"""

	bot.send_message(parse_mode="HTML",chat_id=update.message.chat_id, text=info_text, reply_text=update.message.chat)

@run_async
def get(bot,update,args,job_queue):
	print(os.getcwd())
	chat_id = update.message.chat_id
	try:
		if len(args) == 1:
			keyword = args[0]
			response= google_images_download.googleimagesdownload()
			arguments = {"keywords":keyword,"limit":1,"no_directory":True}
			paths = response.download(arguments)
			bot.send_message(chat_id, text= "wait for some seconds")
			sleep(0.5)
			for i in os.listdir("/app/downloads/"):
				nome = str(i)				
				dic = os.getcwd() + "/downloads/" + nome
				if nome.endswith("gif"):
					bot.sendDocument(chat_id=chat_id, document=open(dic,"rb"))
				else:	
					bot.send_photo(chat_id, photo=open(dic,"rb"))
				os.remove(f"{dic}")

		elif len(args) == 2:
			keyword = args[0]
			sufkey = args[1]
			response= google_images_download.googleimagesdownload()
			arguments = {"keywords":keyword,"suffix_keywords":sufkey,"limit":1,"no_directory":True}
			paths = response.download(arguments)
			bot.send_message(chat_id, text= "wait for some seconds")
			sleep(0.5)
			for i in os.listdir("/app/downloads/"):
				nome = str(i)
				dic = os.getcwd() + "/downloads/" + nome
				if nome.endswith("gif"):
					bot.sendDocument(chat_id=chat_id, document=open(dic,"rb"))
				else:	
					bot.send_photo(chat_id, photo=open(dic,"rb"))
				os.remove(f"{dic}")

		else:
			prekey = args[0]
			keyword = args[1]
			sufkey = args[2]
			response= google_images_download.googleimagesdownload()
			arguments = {"keywords":keyword,"suffix_keywords":sufkey,"prefix_keywords":prekey,"limit":1,"no_directory":True}
			paths = response.download(arguments)
			bot.send_message(chat_id, text= "wait for some seconds")
			sleep(0.5)
			for i in os.listdir("/app/downloads/"):
				nome = str(i)
				dic = os.getcwd() + "/downloads/" + nome
				if nome.endswith("gif"):
					bot.sendDocument(chat_id=chat_id, document=open(dic,"rb"))
					
				else:	
					bot.send_photo(chat_id, photo=open(dic,"rb"))
				os.remove(f"{dic}")

	except IndexError as e:
		bot.send_message(chat_id=chat_id,text="Error none arguments")
		print(f"some error we have here dev look at here {e}")
		

def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help",  ajuda))
	dp.add_handler(CommandHandler("freegames", crawler))
	dp.add_handler(CommandHandler("info", info))
	dp.add_handler(CommandHandler("get", get, pass_args=True,pass_job_queue=True))
	j = dp.job_queue
	job_minute = j.run_once(get,25)
	
	updater.start_polling()
	run(updater)

if __name__== "__main__":
	main()
"""/TODO add new feature google reverse image """