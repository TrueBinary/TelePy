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
from time import sleep
import json
import re 
import logging
import praw
import socket,os,sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, DelayQueue
from telegram.ext.dispatcher import run_async
from google_images_download import google_images_download

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.DEBUG)

logger = logging.getLogger(__name__)
MODE = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")
#fgs = FreeGamesOnSteam subreddits
fgslist = []
#fgf = FreeGamesFindings subreddits
fgflist = []
fgsid = []
fgfid = []
dbfgs = "dbfgs.txt"
dbfgf = "dbfgf.txt"

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


def info(bot,update):
	info_text = """
<b>Hi i'm bot of MrTrue,i was created to help you find some imagens on the google</b>
<b>Developer: </b> <a href="https://t.me/Mr_True">MrTrue</a>
<b>Code: </b> <a href="https://github.com/TrueBinary/TelePy">Github</a>
	"""

	bot.send_message(parse_mode="HTML",chat_id=update.message.chat_id, text=info_text, reply_text=update.message.chat)
	
@run_async
def send_reddit(bot,update):

	reddit = praw.Reddit(client_id=CLIENT_ID,
						client_secret=CLIENT_SECRET,
						user_agent=USER_AGENT)
	chatid = "@FreeeGamesOnSteam"
	subreddit = reddit.subreddit("FreeGamesOnSteam")
	subreddit1 = reddit.subreddit("FreeGameFindings")
	#checa se o id do post esta dentro do arquivo
	def fileindb(fgsid,fgfid):
		found = False
		with open(dbfgs,"r+") as fgsdb, open(dbfgf,"r+") as fgfdb:
			filelist = fgsdb.readlines()
			filelist1 = fgfdb.readlines()
			fgsdb.close()
			fgfdb.close()
		#verifica dentro do arquivo se o id já foi listado
		#se for falso ele ira retornar false e o id sera gravado
		#se for verdadeiro o id não será gravado é o bot continuara segundo
			
			if fgsid not in filelist:
				if fgfid not in filelist1:
					found = False
			else:
				found = True
			return found
	#verifica se o id esta dentro da lista
	def insubreddit(fgsdata,fgfdata):
		if fgsdata in fgsid:
			if fgfdata in fgfid:
				return True
	#deleta as listas para evitar que fiquem duplicadas 
	def datadel():
		del fgslist[:]
		del fgflist[:]
		del fgsid[:]
		del fgfid[:]
	#confere se realmente já foi mandado ou não para o canal 
	def check():
		links = fgsid
		rids = fgfid
		for link in links:
			for rid in rids:
				fgsdata = link[:]
				fgfdata = rid[:]
				if fileindb(fgsdata,fgfdata):
					sleep(560)
					pass
				else: #a função fileindb não conseguir encontrar o id tudo que estiver em fgslist e fgflist será mandado para o seu cana
					if insubreddit(fgsdata,fgfdata):
						with open(dbfgs,"a") as fgsdb, open(dbfgf,"a") as fgfdb:
							fgsdb.writelines("\n"+str(fgsdata))
							fgfdb.writelines("\n"+str(fgfdata))
							fgsdb.close()
							fgfdb.close()
						#se não estiver id não estiver dentro da lista ele ira ser gravado
							fgsfilt = "\n"+str(fgslist).replace("]"," ").replace("["," ").replace("'"," ").replace(","," ")
							fgffilt = "\n"+str(fgflist).replace("]"," ").replace("["," ").replace("'"," ").replace(","," ")
							bot.send_message(chat_id=chatid, text=fgsfilt)
							bot.send_message(chat_id=chatid, text=fgffilt)
							sleep(560)

	while True:
		datadel()
		for submission in subreddit.top("hour"):
			if submission.title not in fgslist[:]:
				fgslist.append([submission.title,submission.url])
				fgsid.append(submission.title)
			elif submission.id in fgsid[:]:
				pass
		for submission in subreddit1.top("hour"):
			if submission.title not in fgflist[:]:
				fgflist.append([submission.title,submission.url])
				fgfid.append(submission.title)
			elif submission.id in fgfid[:]:
				pass	
		check()
		sleep(560)
		continue




def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help",  ajuda))
	dp.add_handler(CommandHandler("info", info))
	dp.add_handler(CommandHandler("steam",send_reddit))
	
	updater.start_polling()
	run(updater)

if __name__== "__main__":
	main()