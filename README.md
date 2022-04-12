# Chia_WebSocket_MQTT
This is test area for me to learn github and practice with my chia-api-> MQTT server. I'm not sure this is going to be helpfull right now to others.  

git clone https://github.com/baerrs/Chia_WebSocket_MQTT.git<br>
cd Chia_WebSocket_MQTT<br>
chmod +x install.sh<br>
./install.sh<br>
<br>
. ./activate<br>
python main.py<br>


I want to get the wallet balacne.  When running this program, if i start Chia's GUI the get_wallet_balance message is brodcasted and I can send read the data and pbulish to the MQTT servetr.  I inishually thought i had to send the request via websockts, but the more I'm reading its a subscirbe/publish websocket broker.  I need to understand how this is being done so I can implement it.  
