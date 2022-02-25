import chia_ws_processing as cp
import json
from datetime import datetime
import inspect
import traceback
import chia_ws_mqtt_messages as ms
import chia.util.misc as chiasub
import logging
import logging.handlers
import os
from config import settings
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
formatter = logging.Formatter('%(asctime)s -%(levelname)s- %(message)s')
logdir = "log/"
if os.path.isdir(logdir):
    pass
else:
    os.mkdir(logdir)
handler = logging.handlers.RotatingFileHandler(
    filename=settings.log_file, maxBytes=(1048576*5), backupCount=7)
handler.setFormatter(formatter)
#sends to stdout
logging.getLogger().addHandler(logging.StreamHandler())
logger.addHandler(handler)
# logging.basicConfig(filename='log/app.log', filemode='w',format='%(asctime)s -%(levelname)s- %(message)s', level=logging.INFO)


def new_farming_info(message, client):
    message_dic ={}
    try:
        dt = str(format(datetime.now()))
        command = message['command']
        passed_filter = message['data']['farming_info']['passed_filter']
        challenge_hash = message['data']['farming_info']['challenge_hash']
        # [2:12]
        proofs = message['data']['farming_info']['proofs']
        signage_point = message['data']['farming_info']['signage_point']
        timestamp = message['data']['farming_info']['timestamp']
        total_plots = message['data']['farming_info']['total_plots']
        destination = message['destination']
        origin = message['origin']
        request_id = message['request_id']
        challenge_hash = str(challenge_hash)[2:10]
        '''
        Create dictionary of message to send to mqtt server
        Edit list to add new fields
        '''
        for variable2publish in ["total_plots", "passed_filter", "challenge_hash", "proofs", "signage_point", "timestamp", "total_plots"]:
            message_dic[variable2publish] = eval(variable2publish)
        ms.message_send(client, message_dic)

        if cp.message_debug[inspect.stack()[0][3]] == "True":
            log_message = '{0}: {1} plots were eligible for farming  {2}... Found {3} proofs'.format(inspect.stack()[0][3],
                                                                                              passed_filter,
                                                                                              challenge_hash, proofs)
            logging.info(log_message)

    except:
        log_message = '{0}: Unhandled new_farming_info message: '.format(inspect.stack()[0][3])
        logging.error(log_message)
        log_message = '{0}: Got message: '.format(datetime.now(), json.dumps(message, indent=4, sort_keys=True))
        logging.error(log_message)
        log_message = '{0}: {1}'.format(inspect.stack()[0][3], traceback.format_exc())
        logging.error(log_message)
        log_message = json.dumps(message)
        logging.error(log_message)


def get_connections(message, client):
    c = 0
    try:
        for messages in message['data']['connections']:
            bytes_read = message['data']['connections'][c]['bytes_read']
            bytes_read = chiasub.format_bytes(bytes_read)
            bytes_written = message['data']['connections'][c]['bytes_written']
            bytes_written = chiasub.format_bytes(bytes_written)
            creation_time = message['data']['connections'][c]['creation_time']
            last_message_time = message['data']['connections'][c]['last_message_time']
            local_port = message['data']['connections'][c]['local_port']
            node_id = message['data']['connections'][c]['node_id']
            peer_host = message['data']['connections'][c]['peer_host']
            if peer_host == '127.0.0.1':
                peak_hash = "null"
                peak_height = "null"
                peak_weight = "null"
                message_dic = {}
                for variable2publish in ["bytes_read", "bytes_written", "last_message_time", "node_id", "peer_host",
                                         "creation_time"]:
                    message_dic[variable2publish] = eval(variable2publish)
                ms.message_send(client, message_dic, c)
                if cp.message_debug[inspect.stack()[0][3]] == "True":
                    log_message = '{0}:  IP address: {1} Read: {2} Written: {3}'.format(inspect.stack()[0][3],
                                                                           peer_host, bytes_read,bytes_written)
                    logging.info(log_message)
            else:
                peak_hash = message['data']['connections'][c]['peak_hash']
                peak_height = message['data']['connections'][c]['peak_height']
                peak_weight = message['data']['connections'][c]['peak_weight']
                message_dic={}
                for variable2publish in ["bytes_read", "bytes_written","last_message_time","node_id","peer_host",
                                         "peak_height","creation_time"]:
                    message_dic[variable2publish] = eval(variable2publish)
                ms.message_send(client, message_dic, c)
                if cp.message_debug[inspect.stack()[0][3]] == "True":
                    log_message = '{0}:  IP address: {1} Peak Height: {2} Read: {3} Written: {4}'.format(inspect.stack()[0][3],
                           peer_host, peak_height,bytes_read,bytes_written)
                    logging.info(log_message)
            ''' ToDo: implement peak_wight '''
            # peak_weight = messages['data']['connections'][c]['peak_weight']
            # print('peak_weight: {0}'.format(peak_weight))
            c += 1
    except Exception as e:
        log_message = '{0}: Unhandled new_farming_info message: '.format(inspect.stack()[0][3])
        logging.error(log_message)
        log_message = e
        logging.error(log_message)
        logging.error(traceback.print_exc())
        log_message = json.dumps(message, indent=4, sort_keys=True)
        logging.error(log_message)


def new_signage_point(message, client):
    message_dic ={}
    command = message['command']
    challenge_chain_sp = message['data']['signage_point']['challenge_chain_sp'][2:12]
    challenge_hash = message['data']['signage_point']['challenge_hash']
    difficulty = message['data']['signage_point']['difficulty']
    reward_chain_sp = message['data']['signage_point']['reward_chain_sp'][2:12]
    signage_point_index = message['data']['signage_point']['signage_point_index']
    sub_slot_iters = message['data']['signage_point']['sub_slot_iters']
    success = message['data']['success']
    destination = message['destination']
    origin = message['origin']
    request_id = message['request_id']

    try:
        for variable2publish in ["challenge_chain_sp", "reward_chain_sp", "signage_point_index", "challenge_chain_sp", "reward_chain_sp"]:
            message_dic[variable2publish] = eval(variable2publish)
        ms.message_send(client, message_dic, c="")
        if cp.message_debug[inspect.stack()[0][3]] == "True":
            log_message = '{0}: finished signage point {1}/64  CC: {2} RC: {3}'.format(inspect.stack()[0][3],
                                                                                signage_point_index, challenge_chain_sp,
                                                                                reward_chain_sp)
            logging.info(log_message)


    except:
        log_message = '{0}: Unhandled new_signage_point message: '.format(inspect.stack()[0][3])
        logging.error(log_message)
        log_message = traceback.print_exc()
        logging.error(log_message)
        log_message = json.dumps(message, indent=4, sort_keys=True)
        logging.error(log_message)


def state_changed(message):
    command = message['command']
    success = message['data']['success']
    destination = message['destination']
    origin = message['origin']
    request_id = message['request_id']
    try:
        if message['data']['state'] == 'new_block':
            if cp.message_debug[inspect.stack()[0][3]] == "True":
                log_message = '{0}: new_block added: {1}'.format(inspect.stack()[0][3], message['request_id'])
                logging.info(log_message)
        elif message['data']['state'] == 'sync_changed':
            if cp.message_debug[inspect.stack()[0][3]] == "True":
                log_message = '{0}: new_block added sync_changed: {1}'.format(inspect.stack()[0][3],
                                                                       message['data']['success'])

    except:
        log_message = '{0}:Unhandled message: {1}'.format(inspect.stack()[0][3])
        logging.error(log_message)
        log_message = traceback.print_exc()
        logging.error(log_message)
        log_message = json.dumps(message, indent=4, sort_keys=True)
        logging.error(log_message)



def register_service(message):
    command = message['command']
    success = message['data']['success']
    destination = message['destination']
    origin = message['origin']
    request_id = message['request_id']
    try:
        if message['request_id'] == '123456ca':
            if cp.message_debug[inspect.stack()[0][3]] == "True":
                log_message = '{0}: Connected to chia_agent service: {1}'.format(inspect.stack()[0][3],
                                                                          message['data']['success'])
                logging.info(log_message)
        elif message['request_id'] == '123456w':
            if cp.message_debug[inspect.stack()[0][3]] == "True":
                log_message = '{0}: Connected to chia_wallet service: {1}'.format(inspect.stack()[0][3],
                                                                           message['data']['success'])
                logging.info(log_message)
        else:
            log_message = '{0}: ***************Unhandled register_service message: {1}'.format(inspect.stack()[0][3],
                                                                           json.dumps(message, indent=4, sort_keys=True))
            logging.error(log_message)

                #
                # print('{0}: {1}: Connected to chia_wallet service: {2}'.format(datetime.now(), inspect.stack()[0][3],
                #                                                            message['data']['success']))
    except:
        # print("x" * 100)
        message = '{1}: Unhandled message: {2}'.format(inspect.stack()[0][3],
                                                        json.dumps(message, indent=4, sort_keys=True))
        logging.error(message)
        # print('{0}: {1}: Unhandled message: {2}'.format(datetime.now(), inspect.stack()[0][3],
        #                                                 json.dumps(message, indent=4, sort_keys=True)))
        # print("x" * 100)


def get_blockchain_state(message, client):

    try:
        command = message['command']
        difficulty = message['data']['blockchain_state']['difficulty']
        genesis_challenge_initialized = message['data']['blockchain_state']['genesis_challenge_initialized']
        mempool_size = message['data']['blockchain_state']['mempool_size']
        challenge_block_info_hash = message['data']['blockchain_state']['peak']['challenge_block_info_hash']
        challenge_vdf_output = message['data']['blockchain_state']['peak']['challenge_vdf_output']['data']
        deficit = message['data']['blockchain_state']['peak']['deficit']
        farmer_puzzle_hash = message['data']['blockchain_state']['peak']['farmer_puzzle_hash']
        fees = message['data']['blockchain_state']['peak']['fees']
        finished_challenge_slot_hashes = message['data']['blockchain_state']['peak']['finished_challenge_slot_hashes']
        finished_infused_challenge_slot_hashes = message['data']['blockchain_state']['peak'][
            'finished_infused_challenge_slot_hashes']
        finished_reward_slot_hashes = message['data']['blockchain_state']['peak']['finished_reward_slot_hashes']
        header_hash = message['data']['blockchain_state']['peak']['header_hash']
        height = message['data']['blockchain_state']['peak']['height']

        if 'infused_challenged_vdf_output' in message['data']['blockchain_state']['peak']:
            if "data" in message['data']['blockchain_state']['peak']['infused_challenge_vdf_output']:
                infused_challenge_vdf_output = message['data']['blockchain_state']['peak']['infused_challenge_vdf_output'][
                    'data']
            else:
                infused_challenge_vdf_output = "N/A"
        else:
            infused_challenge_vdf_output = "N/A"
        overflow = message['data']['blockchain_state']['peak']['overflow']
        pool_puzzle_hash = message['data']['blockchain_state']['peak']['pool_puzzle_hash']
        prev_hash = message['data']['blockchain_state']['peak']['prev_hash']
        prev_transaction_block_hash = message['data']['blockchain_state']['peak']['prev_transaction_block_hash']
        prev_transaction_block_height = message['data']['blockchain_state']['peak']['prev_transaction_block_height']
        required_iters = message['data']['blockchain_state']['peak']['required_iters']
        reward_claims_incorporated = message['data']['blockchain_state']['peak']['reward_claims_incorporated']
        reward_infusion_new_challenge = message['data']['blockchain_state']['peak']['reward_infusion_new_challenge']
        signage_point_index = message['data']['blockchain_state']['peak']['signage_point_index']
        sub_epoch_summary_included = message['data']['blockchain_state']['peak']['sub_epoch_summary_included']
        sub_slot_iters = message['data']['blockchain_state']['peak']['sub_slot_iters']
        timestamp = message['data']['blockchain_state']['peak']['timestamp']
        total_iters = message['data']['blockchain_state']['peak']['total_iters']
        # weight = message['data']['blockchain_state']['peak']['weight']
        space = message['data']['blockchain_state']['space']
        space = chiasub.format_bytes(space)
        sub_slot_iters = message['data']['blockchain_state']['sub_slot_iters']
        sync_mode = message['data']['blockchain_state']['sync']['sync_mode']
        sync_progress_height = message['data']['blockchain_state']['sync']['sync_progress_height']
        sync_tip_height = message['data']['blockchain_state']['sync']['sync_tip_height']
        synced = message['data']['blockchain_state']['sync']['synced']
        success = message['data']['success']
        destination = message['destination']
        origin = message['origin']
        request_id = message['request_id']
        peak_height = message['data']['blockchain_state']['peak']['height']
        if "weight" in message['data']['blockchain_state']['peak']:
            weight = message['data']['blockchain_state']['peak']['weight']
        else:
            weight = "N/A"
        header_hash = message['data']['blockchain_state']['peak']['header_hash'][2:]
        forked = int(message['data']['blockchain_state']['peak']['height']) - 1
        rh = message['data']['blockchain_state']['peak']['reward_infusion_new_challenge'][2:]
        total_iters = message['data']['blockchain_state']['peak']['total_iters']
        overflow = message['data']['blockchain_state']['peak']['overflow']
        deficit = message['data']['blockchain_state']['peak']['deficit']
        difficulty = message['data']['blockchain_state']['difficulty']
        sub_slot_iters = message['data']['blockchain_state']['peak']['sub_slot_iters']
        '''
        I don't know where to get the following values from.  They show up sometimes debug.log as "No Tx".  
        '''
        generator_size = "??"
        generator_ref_list_size = "??"
        header_hash = header_hash[:6]
        rh = rh[:6]
        message_dic ={}
        for variable2publish in ["mempool_size","space", "peak_height", "weight", "header_hash", "forked", "difficulty","sub_slot_iters"]:
            message_dic[variable2publish] = eval(variable2publish)
        ms.message_send(client, message_dic, c="")
        if cp.message_debug[inspect.stack()[0][3]] == "True":
            message = '{0}: height {1}, weight {2}, hh {3} forked at {4}, rh {5}, total iters: {6}, overflow: {7}, deficit: {8}, difficulty: {9}, sub slot iters: {10}, Generator size: {11}, Generator ref list size: {12}'.format(inspect.stack()[0][3], peak_height, weight, header_hash, forked, rh, total_iters,
                    overflow, deficit,
                    difficulty, sub_slot_iters, generator_size, generator_ref_list_size)
            logging.info(message)


    except:
        message = '{0}: Got message:'.format(inspect.stack()[0][3])
        logging.error(json.dumps(message, indent=4, sort_keys=True))
        logging.error(traceback.format_exc())


def get_height_info(message):
    try:
        command = message['command']
        height= message['data']['height']
        destination = message['destination']
        origin = message['origin']
        request_id = message['request_id']
        if cp.message_debug[inspect.stack()[0][3]] == "True":
            # print('{0}: get_height_info:  command: {1}, height: {2}, destination: {3}, origin: {4}, request_id: {5}'.format(datetime.now(), command, height, destination, origin, request_id))
            message = 'get_height_info:  height: {0}, destination: {1}, origin: {2}, request_id: {3}'.format(height, destination, origin, request_id)
            logging.info(message)
    except:
        message = 'unhandled error message in:{0}'.format(datetime.now(), inspect.stack()[0][3])
        logging.error(json.dumps(message, indent=4, sort_keys=True))
        logging.error(traceback.format_exc())
        # print("x" * 100)
        # print('{0}:  unhandled error message in:{1}'.format(datetime.now(), inspect.stack()[0][3]))
        # print(json.dumps(message, indent=4, sort_keys=True))
        # print("x" * 100)
        # traceback.print_exc()
        # print("x" * 100)

def get_wallet_balance(message, client):
    try:
        command = message['command']
        balance = message['data']['wallet_balance']['confirmed_wallet_balance']
        destination = message['destination']
        origin = message['origin']
        request_id = message['request_id']
        if cp.message_debug[inspect.stack()[0][3]] == "True":
            message = '{0}: get_wallet_balance:  command: {1}, balance: {2}, destination: {3}, origin: {4}, request_id: {5}'.format(datetime.now(), command, balance, destination, origin, request_id)
            logging.info(message)
        message_dic ={}
        for variable2publish in ["balance"]:
            message_dic[variable2publish] = eval(variable2publish)
        ms.message_send(client, message_dic, c="")
    except:
        message = '{0}: Got message:'.format(inspect.stack()[0][3])
        logging.error(json.dumps(message, indent=4, sort_keys=True))
        logging.error(traceback.format_exc())




def get_unfinished_block_headers(message):
    if cp.message_debug[inspect.stack()[0][3]] == "True":
        # print('{0}: get_unfinished_block_headers:  ---------------- Not implemented ----------------'.format(datetime.now()))
        message = 'get_unfinished_block_headers:  ---------------- Not implemented ----------------'
        logging.error(message)
        # print(json.dumps(message))
        # print("x" * 100)

def get_unfinished_block_headersf(message):
    if cp.message_debug[inspect.stack()[0][3]] == "True":
        message = 'get_unfinished_block_headers:  --------------- Not implemented ----------------'
        logging.error(message)
        # print(json.dumps(message))
        # print("x" * 100)


def get_blocks(message):
    if cp.message_debug[inspect.stack()[0][3]] == "True":
        message = 'get_blocks:  --------------------------------- Not implemented ----------------'
        logging.error(message)
        # print(json.dumps(message))
        # print("x" * 100)