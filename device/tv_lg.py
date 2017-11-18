import re
import socket
from pylgtv import WebOsClient


def search_device_on_newtork():
  attempts = 10
  request = 'M-SEARCH * HTTP/1.1\r\n' \
                    'HOST: 239.255.255.250:1900\r\n' \
                    'MAN: "ssdp:discover"\r\n' \
                    'MX: 2\r\n' \
                    'ST: urn:schemas-upnp-org:device:MediaRenderer:1\r\n\r\n'

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.settimeout(1)
  tv_ip_address = None
  while attempts > 0:
      sock.sendto(request.encode(), ('239.255.255.250', 1900))
      try:
          response, address = sock.recvfrom(512)
      except:
          attempts -= 1
          continue
      if re.search('LG', response.decode()):
          tv_ip_address = address[0]
          break
      attempts -= 1
  sock.close()
  return tv_ip_address



class WebOsClientEx(WebOsClient):
    def __init__(self):
        ip_address = search_device_on_newtork()
        super(WebOsClientEx, self).__init__(ip_address)

    def turn_on_using_cec(self):
        """CEC method demand the device running this code connected to TV using HDMI cable
           Your TV need support this command to do this, sometimes only one of HDMI ports has this support.
           Search for it on TV configuration.

           Get dependencies on: https://github.com/trainman419/python-cec
        """
        import cec

        cec.init()
        tv = cec.Device(cec.CECDEVICE_TV)
        if not tv.power_on():
            print('The device running this code must be connected to TV using HDMI cable')
            return False
        self.__init__()
        return True

    def turn_on_using_wake_on_lan(self, device_mac_address):
        """Wake On Lan  method demand the device running this code and TV on the same network.
           Your TV need support this command to do this.
           Search for it on TV configuration.

           Get dependencies on: pip install wakeonlan
        """
        from wakeonlan import wol

        wol.send_magic_packet(device_mac_address.replace(':', '.'))