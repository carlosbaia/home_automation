from pylgtv import WebOsClient
import util.tv


def get_tv():
    ip_address = util.tv.search_lg_tv_on_newtork()
    if ip_address:
        tv = WebOsClient(ip_address)
        if not tv.is_registered():
            tv.register()
        return tv
    return None


def on_message(message):
    tv = get_tv()
    if message == 'power:on':
        if tv:
            return True
        return util.tv.turn_on_using_cec()
    elif message == 'power:off':
        if tv:
            tv.power_off()
        return True
    if tv:
        if message == 'mute:on':
            tv.set_mute(True)
        elif message == 'mute:off':
            tv.set_mute(False)
        elif message.startswith('volume:'):
            _, volume = message.split(':')
            if volume.isnumeric():
                tv.set_volume(int(volume))
        elif message.startswith('input:'):
            _, input = message.split(':')
            tv.set_input()
        return True
    return False
