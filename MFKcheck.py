import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time # Модуль для остановки программы
import datetime
import telebot


bot = telebot.TeleBot("2001618640:AAE-bA_qXoY878BTKFj3iNFbMFXS8PfBaEE", parse_mode=None)

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
			self.send_message(str("Cвободные места на курсе " + self.Name_SITE + " : " + str(places[1] - places[0])))
		else:
			print("Мест на " + self.Name_SITE +  " нет	", end='')
		print(self.current_places)

	# Отправка почты через SMTP
	def send_message(self, text):
		bot.send_message(354494423,text)

# Создание объекта и вызов метода

SQL = Free_Places('SQL      ')
PYTHON = Free_Places('PYTHON   ')
DIGITALEC = Free_Places('DIGITALEC')
STARTBUIS = Free_Places('STARTBUIS')
TELEVISAI = Free_Places('TELEVISAI')

while True:
	now = datetime.datetime.now()
	print(str(now.hour)+":"+str(now.minute))
	SQL.check_free()
	PYTHON.check_free()
	DIGITALEC.check_free()
	STARTBUIS.check_free()
	TELEVISAI.check_free()
	time.sleep(90) # Засыпание программы на 3 секунды