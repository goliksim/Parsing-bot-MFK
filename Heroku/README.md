ps -eF

cd /home/golik19266/
nano MFKcheck.py


cd /etc/systemd/system
sudo nano bot.service

sudo systemctl daemon-reload
sudo systemctl enable bot

sudo systemctl start bot
sudo systemctl status bot
sudo systemctl stop bot