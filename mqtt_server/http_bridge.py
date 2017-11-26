import argparse
from flask import Flask, request, jsonify
import paho.mqtt.publish as paho


app = Flask('http_bridge')
args = None


def get_value(content, name, default_value=None):
    if name in content:
        return content[name]
    return default_value


@app.route('/mqtt', methods = ['POST'])
def mqtt():
    content = request.get_json()
    print('[MESSAGE] {}'.format(content))
    try:
        paho.single(get_value(content, 'topic'),
                    get_value(content, 'payload'),
                    qos=get_value(content, 'qos', 2),
                    retain=get_value(content, 'retain', True),
                    hostname=args.mqtt_server_ip,
                    port=args.mqtt_server_port)
    except Exception as ex:
        print('[ERROR]', str(ex))
        return jsonify(status='Error', description=str(ex))
    print('[SUCCESS] Message published')
    return jsonify(status='Published')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mqtt_server_ip', help='IP for MQTT Server', type=str, default='0.0.0.0')
    parser.add_argument('--mqtt_server_port', help='Port for MQTT Server', type=int, default=1883)
    args = parser.parse_args()

    print('Connecting on {}:{}...'.format(args.mqtt_server_ip, args.mqtt_server_port))
    app.run(debug=True, host='0.0.0.0')
