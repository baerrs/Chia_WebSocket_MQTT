from config import settings

def message_send(client, message_dic, c=""):
    for key, value in message_dic.items():
        mqtt_base_topic = settings.mqtt_header
        if c == "":
            mqtt_topic = mqtt_base_topic + "{0}" .format(key)
        else:
            mqtt_base_topic =  settings.mqtt_header + str(c) + "/"
            mqtt_topic = mqtt_base_topic + "{0}" .format(key)
        client.publish(mqtt_topic, value)

# def message_send_2(client, message_dic,c):
#     for key, value in message_dic.items():
#         mqtt_base_topic = "chia_ws/connections/"+str(c)+"/"
#         mqtt_topic = mqtt_base_topic +"{0}".format(key)
#         client.publish(mqtt_topic, value)