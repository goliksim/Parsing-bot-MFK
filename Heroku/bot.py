import os
import requests
import telebot
from flask import Flask , request
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time # Модуль для остановки программы
import datetime

TOKEN = "yourtelebotID"
APP_URL = f'https://mfkbot.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200

Site_Dict = {
    'SQL      '    : 'https://lk.msu.ru/course/view?id=2226',
    'PYTHON   ' : 'https://lk.msu.ru/course/view?id=2387',
	'DIGITALEC' : 'https://lk.msu.ru/course/view?id=2308',
	'STARTBUIS' : 'https://lk.msu.ru/course/view?id=2309',
	'TELEVISAI' : 'https://lk.msu.ru/course/view?id=2360'
}
# Основной класс
class Free_Places:
	# Имя отслеживаемого Мфк
	Name_SITE = ''
	# Ссылка на нужную страницу
	SITE_LINK = ''
	# Заголовки для передачи вместе с URL
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4660.2 Safari/537.36'}
	#текст с количеством занятых и свободных мест
	current_places = ""
	last_places = 0

	def __init__(self, name):
		# Установка курса валюты при создании объекта	
		self.Name_SITE = name
		self.SITE_LINK = Site_Dict[self.Name_SITE]
		self.current_places = self.get_places()

	# Метод для получения курса валюты
	def get_places(self):
		# Парсим всю страницу
		full_page = requests.get(self.SITE_LINK, headers=self.headers)

		# Разбираем через BeautifulSoup
		soup = BeautifulSoup(full_page.content, 'html.parser' )

		# Получаем нужное для нас значение и возвращаем его
		convert = soup.findAll("div", {"class": "well"})

		places_text= convert[0].text.split("мест")
		places_text=places_text[3].replace(' ','').replace('\n','')
		self.current_places = places_text
		return(places_text)

	# Проверка изменения валюты
	def check_free(self):
		places = self.get_places()
		places = places.split('/')
		places = [int(i) for i in places]
		if places[0] < places[1]:
			print("Cвободные места на курсе " + self.Name_SITE + " : " + str(places[1] - places[0])+"	")
			if not places[0]==self.last_places:
				self.send_message(str("Cвободные места на курсе " + self.Name_SITE + " : " + str(places[1] - places[0])))
		else:
			print("Мест на " + self.Name_SITE +  " нет	", end='')
		print(self.current_places)
		self.last_places = places[0]
	# Отправка почты через SMTP
	def send_message(self, text):
		bot.send_message(354494423,text)

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
