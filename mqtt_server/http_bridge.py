import argparse
from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt


mqtt_client = mqtt.Client()
app = Flask('http_bridge')


def get_value(content, name, default_value=None):
    if name in content:
        return content[name]
    return default_value


@app.route('/mqtt', methods = ['POST'])
def mqtt():
    content = request.get_json()
    print('MESSAGE {}'.format(content))
    info = mqtt_client.publish(get_value(content, 'topic'),
                               get_value(content, 'payload'),
                               get_value(content, 'qos', 0),
                               get_value(content, 'retain', False))
    return jsonify(rc=info.rc, is_published=info.is_published())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mqtt_broker', help='IP for MQTT Broker', type=str, default='127.0.0.1')
    parser.add_argument('--mqtt_broker_port', help='Port for MQTT Broker', type=int, default=1883)
    args = parser.parse_args()

    print('Connecting on {}:{}...'.format(args.mqtt_broker, args.mqtt_broker_port))
    if mqtt_client.connect(args.mqtt_broker, args.mqtt_broker_port, 60) == 0:
        app.run(debug=True, host='0.0.0.0')
    else:
        print('Server not found!')
        exit(1)