#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time # Модуль для остановки программы
import datetime
import telebot

# 731275374 - мой айди пользователя
# 354494423 - айди друга

bot = telebot.TeleBot("yourtelebotID")

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.chat.id, 'Здравствуй')


@bot.message_handler(content_types=['text'])
def lalala(message):
	bot.send_message(message.chat.id,str(message.chat.id))


#Run

# Словарь с ссылками на сайты курсов МФК
Site_Dict = {
    'SQL      '    : 'https://lk.msu.ru/course/view?id=2226',
    'PYTHON   ' : 'https://lk.msu.ru/course/view?id=2387',
	'DIGITALEC' : 'https://lk.msu.ru/course/view?id=2308',
	'STARTBUIS' : 'https://lk.msu.ru/course/view?id=2309',
	'TELEVISAI' : 'https://lk.msu.ru/course/view?id=2360',
	'POVEDENEC' : 'https://lk.msu.ru/course/view?id=2316'
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
			#print("Cвободные места на курсе " + self.Name_SITE + " : " + str(places[1] - places[0])+"	")
			if  places[0]< self.last_places and places[0]>places[1]-5:
				if self.Name_SITE == 'POVEDENEC':
					self.send_message(731275374,str("Cвободные места на курсе " + self.Name_SITE + " : " + str(places[1] - places[0])+"     "+ str(self.SITE_LINK)))
				else:
					self.send_message(354494423,str("Cвободные места на курсе " + self.Name_SITE + " : " + str(places[1] - places[0])+"	"+ str(self.SITE_LINK)))
		#else:
			#print("Мест на " + self.Name_SITE +  " нет	", end='')
		#print(self.current_places)
		self.last_places = places[0]
	# Отправка
	def send_message(self,id, text):
		bot.send_message(id,text)

# Создание объекта и вызов метода
if __name__ == '__main__':
	SQL = Free_Places('SQL      ')
	PYTHON = Free_Places('PYTHON   ')
	DIGITALEC = Free_Places('DIGITALEC')
	#STARTBUIS = Free_Places('STARTBUIS')
	#TELEVISAI = Free_Places('TELEVISAI')
	#POVEDENEC = Free_Places('POVEDENEC')
	while True:
		now = datetime.datetime.now()
		#print(str(now.hour)+":"+str(now.minute))
		SQL.check_free()
		PYTHON.check_free()
		DIGITALEC.check_free()
		#STARTBUIS.check_free()
		#TELEVISAI.check_free()
		#POVEDENEC.check_free()
		time.sleep(3) # Засыпание программы на 3 секунды

