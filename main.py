import  paho.mqtt.client as mqtt
import time
import traceback
import inspect
import os
import ssl
import websocket
import json
from datetime import datetime
import chia_ws_commands as chia_ws_commands
import logging

logging.basicConfig(filename='log/app.log', filemode='w',format='%(asctime)s -%(levelname)s- %(message)s', level=logging.INFO)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        message = "connected OK Returned code={0}".format(rc)
        logging.info(message)
        # logging.debug('This is a debug message')
        # logging.info('This is an info message')
        # logging.warning('This is a warning message')
        # logging.error('This is an error message')
        # logging.critical('This is a critical message')
        #client.subscribe(topic)
    else:
        message = "Bad connection Returned code={0}".format(rc)
        logging.error(message)


# websocket.enableTrace(True)
def on_message(ws, message):
    message = json.loads(message)
    command = message['command']
    if command == 'new_farming_info':
        chia_ws_commands.new_farming_info(message, client)
    elif command == 'get_connections':
        chia_ws_commands.get_connections(message, client)
    elif command == 'new_signage_point':
        chia_ws_commands.new_signage_point(message, client)
    elif command == 'state_changed':
        chia_ws_commands.state_changed(message)
    elif command == 'register_service':
        chia_ws_commands.register_service(message)
    elif command == 'get_blockchain_state':
        chia_ws_commands.get_blockchain_state(message, client)
    elif command == 'get_unfinished_block_headers':
        chia_ws_commands.get_unfinished_block_headers(message)
    elif command == 'get_signage_points':
        x=1
    # {'ack': True, 'command': 'get_signage_points', 'data': {'signage_points': [], 'success': True},
    #  'destination': 'wallet_ui', 'origin': 'chia_farmer',
    #  'request_id': 'bb42b842170b16a7fd1f38de84d16587f046e13b3fb6ada506b3e4d7fdbd1979'}
    elif command == 'ping':
        x=1
    elif command == 'get_sync_status':
        x = 1
    # ping
    # {'ack': True, 'command': 'ping', 'data': {'success': True}, 'destination': 'wallet_ui', 'origin': 'chia_harvester',
    #  'request_id': '70e28864ad9e5823c427b65d13c4f48a64d8b3661162746113539641afa17c7b'}
    #
    elif command == 'get_harvesters':
        x=1
    # {'ack': True, 'command': 'get_harvesters', 'data': {'harvesters': [], 'success': True}, 'destination': 'wallet_ui',
    #  'origin': 'chia_farmer', 'request_id': '415c7fc16a05e87724b3d7e4c9ce2e3b7badbe620a04d65b732e01047e2d7987'}
    #
    elif command == 'get_plot_directories':
        x=1
    # {'ack': True, 'command': 'get_plot_directories', 'data': {'directories': ['C:\\chia-plot'], 'success': True},
    #  'destination': 'wallet_ui', 'origin': 'chia_harvester',
    #  'request_id': '41291d340c2c7cd4917200242f2fba32cb890c483c87f7fe4ef0ba26fca612fc'}
    #
    elif command == 'get_plots':
        x=1
    elif command =='get_public_keys':
        x=1
    # {'ack': True, 'command': 'get_public_keys',
    #  'data': {'public_key_fingerprints': [2817487474, 123781786], 'success': True}, 'destination': 'wallet_ui',
    #  'origin': 'chia_wallet', 'request_id': '2d3407cda8aa1f5501c03ebe3d5e8e9a7feec6730eea248ec8941cb5f2a8601f'}

    elif command == 'log_in':
        x=1
    # {'ack': True, 'command': 'log_in', 'data': {'fingerprint': 2817487474, 'success': True}, 'destination': 'wallet_ui',
    #  'origin': 'chia_wallet', 'request_id': '0a263e961e39360916366e63bfa6dfcba6d7a67dcdfae21890fbac17cbb8aa60'}

    elif command == 'get_wallets':
        x=1
    # {'ack': True, 'command': 'get_wallets',
    #  'data': {'success': True, 'wallets': [{'data': '', 'id': 1, 'name': 'Chia Wallet', 'type': 0}]},
    #  'destination': 'wallet_ui', 'origin': 'chia_wallet',
    #  'request_id': 'e47fa670c813e8bdc7aa4cd0424ae745bb4c8679431125bd1774491499ea736f'}

    elif command == 'get_network_info':
        x=1
    # {'ack': True, 'command': 'get_network_info',
    #  'data': {'network_name': 'mainnet', 'network_prefix': 'xch', 'success': True}, 'destination': 'wallet_ui',
    #  'origin': 'chia_wallet', 'request_id': '6192712fccbee44196f70be54dba7dec316b2404d12c56423181970db1ce1e9b'}

    elif command == 'get_all_trades':
        x=1
    # {'ack': True, 'command': 'get_all_trades', 'data': {'success': True, 'trades': []}, 'destination': 'wallet_ui',
    #  'origin': 'chia_wallet', 'request_id': '13d87cece0ea69e548b7323c21b789e260ebd44cc9bfbbadd29d0fb56c4f3b90'}

    elif command == 'get_farmed_amount':
        x=1
    # {'ack': True, 'command': 'get_farmed_amount',
    #  'data': {'farmed_amount': 0, 'farmer_reward_amount': 0, 'fee_amount': 0, 'last_height_farmed': 0,
    #           'pool_reward_amount': 0, 'success': True}, 'destination': 'wallet_ui', 'origin': 'chia_wallet',
    #  'request_id': 'a8270cc618a2e9dfcd773337af373ec0c845b13fd744eb5b1dfdbf8981f4ae43'}

    elif command == 'get_wallet_balance':
        x=1
    # {'ack': True, 'command': 'get_wallet_balance', 'data': {'success': True,
    #                                                         'wallet_balance': {'confirmed_wallet_balance': 0,
    #                                                                            'max_send_amount': 0,
    #                                                                            'pending_change': 0,
    #                                                                            'pending_coin_removal_count': 0,
    #                                                                            'spendable_balance': 0,
    #                                                                            'unconfirmed_wallet_balance': 0,
    #                                                                            'unspent_coin_count': 0,
    #                                                                            'wallet_id': 1}},
    #  'destination': 'wallet_ui', 'origin': 'chia_wallet',
    #  'request_id': '71ddf8ce6309bd323b9660d924114b5b52ccb4f42e60f55d2a830859fa03fba2'}

    elif command == 'get_transactions':
        x=1
    # {'ack': True, 'command': 'get_transactions', 'data': {'success': True, 'transactions': [], 'wallet_id': 1},
    #  'destination': 'wallet_ui', 'origin': 'chia_wallet',
    #  'request_id': '3710dc313571f99ed3ba31f1c60fdfbbedda9dd41c0a6a327090df01ba4ba30a'}

    elif command == 'get_next_address':
        x=1
    # {'ack': True, 'command': 'get_next_address',
    #  'data': {'address': 'xch1tvkl7x53dvksdev3jcx72ykfujklshcu37r0fuldgjd48r03sdhqzumz7t', 'success': True,
    #           'wallet_id': 1}, 'destination': 'wallet_ui', 'origin': 'chia_wallet',
    #  'request_id': 'e015e25204f221f25139c6ae4d77ccacbe8c791d3b0907983f841f569e44df6e'}

    elif command == 'get_public_keys':
        x=1
    # {'ack': True, 'command': 'get_public_keys',
    #  'data': {'public_key_fingerprints': [2817487474, 123781786], 'success': True}, 'destination': 'wallet_ui',
    #  'origin': 'chia_wallet', 'request_id': '359967a5044423e29b27c99548f38174330bed26e7d2256060e25cbf112826f1'}

    # {'ack': False, 'command': 'get_plots', 'data': {'failed_to_open_filenames': [], 'not_found_filenames': [],
    # 'plots': [{'file_size': 108801343425, 'filename':
    # 'C:\\chia-plot\\plot-k32-2021-06-18-16-12-db837e16d624f77eaa12ead6df938598c154ef7f441a465f7932a004fd1675f3.plot
    # ', 'plot-seed': '0xdb837e16d624f77eaa12ead6df938598c154ef7f441a465f7932a004fd1675f3', 'plot_id':
    # '0xdb837e16d624f77eaa12ead6df938598c154ef7f441a465f7932a004fd1675f3', 'plot_public_key':
    # '0xa5be6b42bb2f0ad9625bb9a6548ab4a3f6a4f97eec146a6d6281f24fc05efe4a9eba3a4ca7bd3dd13e2bccaa9a2fbedd',
    # 'pool_contract_puzzle_hash': None, 'pool_public_key':
    # '0x90b7213459169dc73b3b62186a0bbd3c7f4f2fe9d9f7b7c4704ab323792fd676ac6faab4b56cb902d1e7dbfc1a6d4468',
    # 'size': 32, 'time_modified': 1624063316.060686}, {'file_size': 108750583724, 'filename':
    # 'C:\\chia-plot\\plot-k32-2021-06-18-20-41-9060682f9d0e1d9a98ad352dce1332f99b5d286ce2bbcbc7ea025ba6612468de.plot
    # ', 'plot-seed': '0x9060682f9d0e1d9a98ad352dce1332f99b5d286ce2bbcbc7ea025ba6612468de', 'plot_id':
    # '0x9060682f9d0e1d9a98ad352dce1332f99b5d286ce2bbcbc7ea025ba6612468de', 'plot_public_key':
    # '0xa126345f6b6573c85c1513c141a4ba61fa8a8e6eb6de7b3f07fd846be6adfabe257f32b8fa09ae51466fd4819b5a13b6',
    # 'pool_contract_puzzle_hash': None, 'pool_public_key':
    # '0x90b7213459169dc73b3b62186a0bbd3c7f4f2fe9d9f7b7c4704ab323792fd676ac6faab4b56cb902d1e7dbfc1a6d4468',
    # 'size': 32, 'time_modified': 1624077721.4887898}, {'file_size': 108836274795, 'filename':
    # 'C:\\chia-plot\\plot-k32-2021-06-19-00-42-84cc472bb6d7c10858ddc441958ef2dcb1514eefb436077024db9ad90654d03f.plot
    # ', 'plot-seed': '0x84cc472bb6d7c10858ddc441958ef2dcb1514eefb436077024db9ad90654d03f', 'plot_id':
    # '0x84cc472bb6d7c10858ddc441958ef2dcb1514eefb436077024db9ad90654d03f', 'plot_public_key':
    # '0x873a367ec95727aa84fb1f92f9111dff4a4addaa1cf7862294db03a0499a7b87172e7a90bf4cb94a776e9835bac1fc06',
    # 'pool_contract_puzzle_hash': None, 'pool_public_key':
    # '0x90b7213459169dc73b3b62186a0bbd3c7f4f2fe9d9f7b7c4704ab323792fd676ac6faab4b56cb902d1e7dbfc1a6d4468',
    # 'size': 32, 'time_modified': 1624092296.6237319}], 'success': True}, 'destination': 'wallet_ui',
    # 'origin': 'chia_harvester', 'request_id': '981f707a86b32d896032d6883c1178f18332f8ffa974a7d3e8f2ae0f514db033'}

    elif command == 'get_blocks':
        chia_ws_commands.get_blocks(message)
    elif command == 'get_height_info':
        chia_ws_commands.get_height_info(message)
    else:
        message = "connected OK Returned code={0}".format(rc)
        #logging.critical("x" * 100)
        logging.critical(message)
        logging.critical(json.dumps(message))
        message ='{0}: Unhandled message: {1}'.format(inspect.stack()[0][3],
                                                        json.dumps(message, indent=4, sort_keys=True))
        logging.critical(message)
        #logging.critical("x" * 100)


def on_error(self, error):
    log_message = 'Error in websocket: {0}'.format(error)
    logging.critical(log_message)


def on_close(self, ws, e):
    log_message = 'Websocket closed: {0}'.format(e)
    logging.info(log_message)


def on_open(self):
    log_message = '{0}: Opening connection to Websocket'.format(inspect.stack()[0][3])
    logging.info(log_message)
    message = {"destination": "daemon", "command": "register_service", "request_id": "123456ca", "origin": "",
               "data": {"service": 'chia_agent'}}
    on_send_message(self, message)
    message = {"destination": "daemon", "command": "register_service", "request_id": "123456w", "origin": "",
               "data": {"service": 'wallet_ui'}}
    on_send_message(self, message)
    message = {"destination": "full_node", "command": "get_blockchain_state", "request_id": "123456ca", "origin": "",
               "data": {"service": 'full_node'}}
    on_send_message(self, message)


def on_send_message(ws, message):
    log_message = '{0}: Sent Message: Registration'.format(inspect.stack()[0][3])
    logging.info(log_message)
    # print('{0}: {1}: Sent Message: Registration'.format(datetime.now(), inspect.stack()[0][3]))
    wsapp.send(json.dumps(message))


def on_ping(ws, data):
    x=1
    # print('{0}: {1}: Got ping'.format(datetime.now(), inspect.stack()[0][3]))



client = mqtt.Client()             #create new instance
client.on_connect=on_connect  #bind call back function
client.connect(host='173.230.128.181', port=1883)               #connect to broker
client.loop_start()  #Start loop
time.sleep(4) # Wait for connection setup to complete
# print("testing")

debug = True


message = "---------------------Starting Chia Websocket Client---------------------"
logging.info(message)
wsapp = websocket.WebSocketApp("wss://localhost:55400",
                               on_open=on_open,
                               on_message=on_message,
                               on_error=on_error,
                               on_ping=on_ping)


key_crt = "ssl/daemon/private_daemon.crt"
private_daemon_key ="ssl/daemon/private_daemon.key"

wsapp.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE, "certfile": key_crt,
                          "keyfile": private_daemon_key, "ssl_context.check_hostname": False})
wsapp.close()




client.loop_stop()    #Stop loop
