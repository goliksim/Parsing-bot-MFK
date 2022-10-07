# Parsing telegram sites by bot.
So, guys, today we will write the simplest telegram bot that will parse the site you need and send a notification to the cart if the value of the number, information, etc. you need changes on it.
## Creating a bot in a cart
- To begin with, the bot itself needs to be created, for this we find in the telegram the father of all bots @BotFather.
- Write to him / start
- Next, create a new bot / newbot
- We give it any name, for example: CheckMfkSql
- And also something like a login. The login must necessarily end with "bot", for example: check_mfk_skl_bot <br />
The bot will send us congratulations on the creation of a new bot, as well as its token, it must be remembered (written down somewhere). <br />
![image](https://user-images.githubusercontent.com/66952748/137626951-c36cc3b6-f4d3-4248-b109-1a2419ce3a29.png )
## Code the bot in Python
Next, let's move on to writing the code for the bot itself. For personal convenience, I wrote it in Python. <br />
At the very beginning, add:
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
```
This is necessary for the program to work correctly in a virtual machine from Google. <br />
Next, we will connect the libraries we need:
```python
import requests # Module for URL processing
from bs4 import BeautifulSoup # Module for working with HTML
import time # Module for stopping
the import datetime
import telebot program
```
Initialize the bot and write commands to work with the bot (spoiler! they won't work since the bot is running in GetHooka mode).

```python
bot = telebot.TeleBot("2001618640:AAE-bA_qXoY878BTKFj3iNFbMFXS8PfBaEE")

@bot.message_handler(commands=['start'])
def welcome(message):
bot.send_message(message.chat.id , 'Hello')


@bot.message_handler(content_types=['text'])
def lalala(message):
bot.send_message(message.chat.id ,str(message.chat.id ))
```
We write down a dictionary of links to the necessary sites (in my case, these are MSU courses and I will parse the same thing meaning on different pages)
```
Site_Dict = {
'SQL ' : 'https://lk.msu.ru/course/view?id=2226',
'PYTHON ' : 'https://lk.msu.ru/course/view?id=2387',
'DIGITALEC' : 'https://lk.msu.ru/course/view?id=2308'
}
```
Next, the main class of working with the site. Each object of the class is a process for parsing a particular site. Comments are present in the code itself
```python
# Main class
class Free_Places:
# Name of the monitored Ifc
Name_SITE = ''
# Link to the desired page
SITE_LINK = ''
# Headers to be transmitted along with the URL
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4660.2 Safari/537.36'}
#text with the number of occupied and free places
current_places = ""
last_places = 0

def __init__(self, name):
# Setting the currency exchange rate when creating an object
self.Name_SITE = name
self.SITE_LINK = Site_Dict[self.Name_SITE]
self.current_places = self.get_places()

# Method for getting the exchange rate
def get_places(self):
# Parse the entire page
full_page = requests.get(self.SITE_LINK, headers=self.headers)

# Disassembling via BeautifulSoup
soup = BeautifulSoup(full_page.content, 'html.parser' )

# Get the value we need and return it
convert = soup.findAll("div", {"class": "well"})

places_text= convert[0].text.split("places")
places_text=places_text[3].replace(' ','').replace('\n','')
self.current_places = places_text
return(places_text)

# Checking currency changes
def check_free(self):
places = self.get_places()
places = places.split('/')
places = [int(i) for i in places]
if places[0] < places[1]:
#print("Free seats on the course " + self.Name_SITE + " : " + str(places[1] - places[0])+" ")
if places[0]< self.last_places and places[0]>places[1]-5:
if self.Name_SITE == 'POVEDENEC':
self.send_message(731275374,str("Free seats on the course " + self.Name_SITE + " : " + str(places[1] - places[0])+" "+ str(self.SITE_LINK)))
else:
self.send_message(354494423,str("Free seats on the course " + self.Name_SITE + " : " + str(places[1] - places[0])+" "+ str(self.SITE_LINK)))
#else:
#print("Places on " + self.Name_SITE + " no ", end=")
#print(self.current_places)
self.last_places = places[0]
# Sending
def send_message(self,id, text):
bot.send_message(id,text)
```
Now let's create our objects and call the update function after a certain period of time.
```python
# Creating an object and calling the method
if __name__ == '__main__':
SQL = Free_Places('SQL')
PYTHON = Free_Places('PYTHON')
DIGITALEC = Free_Places('DIGITALEC')
while True:
now = datetime.datetime.now()
#print(str(now.hour)+":"+str(now.minute))
SQL.check_free()
PYTHON.check_free()
DIGITALEC.check_free()
time.sleep(3) # Program falling asleep for 3 seconds
```
Great! The bot code is written.
## Creating a virtual machine from Google
In order for the program to work constantly without our presence, you need to upload it to the server. In this case, I will use a virtual machine from Google, since it allows me to host my code for free for 3 months. <br />
We go to https://console.cloud .google.com/getting-started. <br />
Register and proceed to the VM instance creation process. <br />
I will use the weakest version of a virtual machine with a server in Finland.<br /><br />
![vm_regionmachine](https://user-images.githubusercontent.com/66952748/137626974-36819da9-b4a9-4215-aa97-7d966ad98977.png)<br />
Choosing a Debian VM.<br /><br />
![vm_bootdisk](https://user-images.githubusercontent.com/66952748/137626964-45ef1db5-0f08-4ef4-8ca7-bd479f7b828d.png)<br />
After creation, you need to connect to our machine via ssh protocol.<br /><br />
![vm_ssh_open](https://user-images.githubusercontent.com/66952748/137626981-cba74fd4-6678-4ee6-b815-43fa568deb04.png)<br />
Go to any folder and create a py file of our bot, we need to transfer our code there.
```
cd /home/yourprofilename/
nano MFKcheck.py
```
The file can also be downloaded via a menu with a gear.
Next, go to the system folder and create a service file.
```
cd /etc/systemd/system
sudo nano bot.service
```
Here we write the following
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
Next, turn on our service
```
sudo systemctl daemon-reload
sudo systemctl enable bot

sudo systemctl start bot
sudo systemctl status bot
```
To update the bot code, first disable the bot, edit the code in the py file, and reboot the bot
```
sudo systemctl stop bot
#edit the py file
sudo systemctl daemon-reload
sudo systemctl start bot
sudo systemctl status bot
```
The end! Your bot is running on a Google virtual machine.
