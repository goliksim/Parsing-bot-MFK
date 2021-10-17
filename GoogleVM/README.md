# Парсинг сайтов телеграмм ботом.
Итак, ребятки, сегодня мы с Вами напишем самого простого телеграм бота, который будет парсить нужный вам сайт и присылать уведомление в телегу, если на нем измениться нужное вам значение числа, информации и т.д.
## Cоздание бота в телеге
- Для начала самого бота нужно создать, для этого в телеграме находим батьку всех ботов @BotFather.
- Пишем ему /start
- Далее создаем нового бота /newbot
- Задаем ему любое название, например: CheckMfkSql
- А также что=то вроде логина. Логин обязательно должен заканчиваться на "bot", к примеру: check_mfk_skl_bot <br />
Бот пришлет нам поздравление с созданием нового бота, а также его токен, его необходимо запомнить (записать куда-нибудь). <br />
![image](https://user-images.githubusercontent.com/66952748/137626951-c36cc3b6-f4d3-4248-b109-1a2419ce3a29.png)
## Кодим бота на Python
Далее перейдем к написанию самого кода для бота. Для личного удобства я писал его на Python. <br />
В самое начало добавьте:
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
```
Это нужно для корректной работы программы в виртуальной машине от Google. <br />
Далее подключим необходимые нам библиотеки:
```python
import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time # Модуль для остановки программы
import datetime
import telebot
```
Инициализируем бота и прописываем команды для работы с ботом (спойлер! они не будут работать так как бот работает в режиме GetHooka).

```python
bot = telebot.TeleBot("2001618640:AAE-bA_qXoY878BTKFj3iNFbMFXS8PfBaEE")

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.chat.id, 'Здравствуй')


@bot.message_handler(content_types=['text'])
def lalala(message):
	bot.send_message(message.chat.id,str(message.chat.id))
```
Записываем словарь ссылок на необходимые сайты (в моем случае это курсы МГУ и парсить я буду одно и тоже значение на разных страничках)
```
Site_Dict = {
    'SQL      '    : 'https://lk.msu.ru/course/view?id=2226',
    'PYTHON   ' : 'https://lk.msu.ru/course/view?id=2387',
	'DIGITALEC' : 'https://lk.msu.ru/course/view?id=2308'
}
```
Далее основной класс работы с сайтом. Каждый объект класса - процесс по парсингу того или иного сайта. Комментарии присутствуют в самом коде 
```python
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
```
Теперь создадим наши объекты и будем вызывать функцию обновления через какой-то промежуток времени.
```python
# Создание объекта и вызов метода
if __name__ == '__main__':
	SQL = Free_Places('SQL      ')
	PYTHON = Free_Places('PYTHON   ')
	DIGITALEC = Free_Places('DIGITALEC')
	while True:
		now = datetime.datetime.now()
		#print(str(now.hour)+":"+str(now.minute))
		SQL.check_free()
		PYTHON.check_free()
		DIGITALEC.check_free()
		time.sleep(3) # Засыпание программы на 3 секунды
```
Отлично! Код бота написан.
## Создание виртуальной машины от Google
Чтобы программа работала постоянно без нашего присутствия нужно залить ее на сервер. В данном случае я буду использовать виртуальную машину от гугл, так как она позволяет 3 месяца хостить мой код бесплатно. <br />
Заходим на https://console.cloud.google.com/getting-started. <br />
Регистрируемся и переходим к этаму создания VM instance.  <br />
Я буду использовать самый слабый вариант виртуальной машины с сервером в Финляндии.<br /><br />
![vm_regionmachine](https://user-images.githubusercontent.com/66952748/137626974-36819da9-b4a9-4215-aa97-7d966ad98977.png)<br />
Выбираем виртуальную машину на Debian.<br /><br />
![vm_bootdisk](https://user-images.githubusercontent.com/66952748/137626964-45ef1db5-0f08-4ef4-8ca7-bd479f7b828d.png)<br />
После создания, нужно подключится к нашей машине по ssh протоколу.<br /><br />
![vm_ssh_open](https://user-images.githubusercontent.com/66952748/137626981-cba74fd4-6678-4ee6-b815-43fa568deb04.png)<br />
Переходим в любую папку и создаем py файл нашего бота, туда нужно перенести наш код.
```
cd /home/yourprofilename/
nano MFKcheck.py
```
Также файл можно загрузить через менюшку с шестеренкой. 
Далее переходим в системную папку и создаем файл сервиса.
```
cd /etc/systemd/system
sudo nano bot.service
```
Здесь пишем следующее
```
[Unit]
Description=Telegram bot 'MFKbot'
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/yourprofilename
ExecStart=/usr/bin/python3 /home/yourprofilename/MFKcheck.py

RestartSec=3
Restart=always

[Install]
WantedBy=multi-user.target

```
Далее включаем наш сервис
```
sudo systemctl daemon-reload
sudo systemctl enable bot

sudo systemctl start bot
sudo systemctl status bot
```
Для обновления кода бота сперва отключаем бота, правим код в py файле, и перезагружаем бота
```
sudo systemctl stop bot
#правка py файла
sudo systemctl daemon-reload
sudo systemctl start bot
sudo systemctl status bot
```
Конец! Ваш бот запущен на виртуальной машине гугла. 
