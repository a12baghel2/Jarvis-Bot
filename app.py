import logging 
from telegram.ext import Updater,CommandHandler,MessageHandler,filters, Application
from flask import Flask,request
from telegram import Bot,Update, ReplyKeyboardMarkup
from utils import get_reply,fetch_status,fetch_weather,fetch_quote,mars,getPic,camera_keyboard,news_topic,get_news

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "965551773:AAELHqZwhLkOReFjlrjSVZQ7fMCKKtPak8k"

app = Flask(__name__)
@app.route(f'/{TOKEN}',methods=['GET','POST'])
def webhook():
	update = Update.de_json(request.get_json(),bot)

	dp.process_update(update)
	return "ok"

def start(bot,update):
	author = update.message.from_user.first_name
	reply = "Hii!! {}".format(author)
	bot.send_message(chat_id=update.message.chat_id,text=reply)

def _help(bot,update):
	help_text = "Hey! Do you need help?\nYou can type 'corona staus in [country name]' and get corona staus of that country. Note: there is problem in fetching United States,Australia and China data\nYou can type /camera and get images from Curiousity Rover.\nYou can type /news to get news by choosing topic available.\nYou can type pic of the day, astronmy pic of the day or astronmy pic from [date] to get a image from nasa.\nOr you could search weather in your city by 'tell me weather in [city_name]'"
	bot.send_message(chat_id = update.message.chat_id,text=help_text)

def camera(bot,update):
	bot.send_message(chat_id=update.message.chat_id,text="Choose a category",reply_markup=ReplyKeyboardMarkup(keyboard=camera_keyboard,one_time_keyboard=True))

def news(bot,update):
	bot.send_message(chat_id=update.message.chat_id,text="Choose a category",reply_markup=ReplyKeyboardMarkup(keyboard=news_topic,one_time_keyboard=True))

async def reply_text(bot,update):
	intent,reply = get_reply(update.message.text,update.message.chat_id)
	print(intent)
	if intent == "corona status":
		status = fetch_status(reply)
		await bot.send_message(chat_id=update.message.chat_id,text=status)
	if intent == "show climate":
		weather = fetch_weather(reply)
		print(reply.get('geo-city'))
		await bot.send_message(chat_id=update.message.chat_id,text=weather)
	if intent == "get_quotes":
		quote = fetch_quote(reply)
		await bot.send_message(chat_id=update.message.chat_id,text=quote)
	if intent == "mars":
		get_info = mars(reply)
		for i in get_info['photos'][:5]:
			sendReply = "Rover Name: {}\nLaunch Date: {}\nLanding Date: {}\nCamera Name: {}\nPicture: {}".format(i['rover']['name'],i['rover']['launch_date'],i['rover']['landing_date'],i['camera']['full_name'],i['img_src'])
			await bot.send_message(chat_id=update.message.chat_id,text=sendReply)
	
	if intent == "planet_pic":
		pic = getPic(reply)
		sendReply = "Date: {}\nCopyright: {}\nDescription:\n{}\nImage: {}".format(pic['date'],pic['copyright'],pic['explanation'],pic['hdurl'])
		await bot.send_message(chat_id=update.message.chat_id,text=sendReply)

	if intent == "get_news":
		news = get_news(reply)
		for i in news[:10]:
			sendReply = "Title: {}\nDescription: {}\nAuthor: {}\nLink: {}".format(i['title'],i['description'],i['author'],i['url'])
			await bot.send_message(chat_id=update.message.chat_id,text=sendReply)

	if intent ==  "small_talk":
		await bot.send_message(chat_id=update.message.chat_id,text=reply)

async def echo_sticker(bot,update):
	await bot.send_sticker(chat_id=update.message.chat_id,sticker=update.message.sticker.file_id)

def error(bot,update):
	logger.error("update '%s' caused error '%s'",update,update.error)

bot = Bot(TOKEN)

try:
	async def set_webhook(): await dp.bot.set_webhook("https://jarvis-bot-omega.vercel.app/"+TOKEN)
except Exception as e:
	print(e)


dp = Application.builder().token(TOKEN).build()
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",_help))
dp.add_handler(CommandHandler("camera",camera))
dp.add_handler(CommandHandler("news",news))
dp.add_handler(MessageHandler(filters.Text,reply_text))
dp.add_handler(MessageHandler(filters.Sticker,echo_sticker))
dp.add_error_handler(error)
set_webhook()
dp.run_polling(0.3)



if __name__ == "__main__":
	app.run(port=8443)
