# git clone https://github.com/eclipse/paho.mqtt.python
# cd paho.mqtt.python
# python setup.py install
import argparse
import paho.mqtt.client as mqtt

import mqtt_tv

devices = {
    'living_room_tv': mqtt_tv.on_message
}


def on_connect(client, user_data, flags, rc):
    print("[STATUS] Connected. Code: {}".format(rc))
    for topic_name in devices.keys():
        client.subscribe(topic_name)


def on_message(client, user_data, msg):
    payload = str(msg.payload.decode())
    print("[MESSAGE] Topic: {} / Message: {}".format(msg.topic, payload))
    success = devices[msg.topic](payload)
    print("[MESSAGE] Execution: {}".format('success' if success else 'error'))


def run(ip_address, port):
    print("[STATUS] Initializing MQTT...")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(ip_address, port, 60)
    client.loop_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mqtt_server_ip', help='IP for MQTT Server', type=str, default='0.0.0.0')
    parser.add_argument('--mqtt_server_port', help='Port for MQTT Server', type=int, default=1883)
    args = parser.parse_args()

    run(args.mqtt_server_ip, args.mqtt_server_port)
