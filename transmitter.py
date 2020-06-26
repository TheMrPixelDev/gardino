from rpi_rf import RFDevice
""""
class transmit:

    def __init__(self, protocol, repeat):
        self.protocol = protocol
        self.rfdevice = RFDevice(17)
        self.rfdevice.enable_tx()
        self.rfdevice.tx_repeat = repeat

        self.devices_turn_on_codes = {
            "1": {"code": 4265041, "length": 317},
            "3": {"code": 4264273, "length": 317},
            "4": {"code": 4261201, "length": 317},
            "5": {"code": 1381719, "length": 356}
        }

        self.devices_turn_off_codes = {
            "1": {"code": 4265044, "length": 317},
            "3": {"code": 4264276, "length": 317},
            "4": {"code": 4261204, "length": 317},
            "5": {"code": 1381716, "length": 356}
        }

    def turn_off(self, device_id):

        self.rfdevice.tx_code(self.devices_turn_off_codes.get(device_id).get("code"), self.protocol, self.devices_turn_off_codes.get(device_id).get("length"), None)
        self.rfdevice.cleanup()

    def turn_on(self, device_id):

        self.rfdevice.tx_code(self.devices_turn_on_codes.get(device_id).get("code"), self.protocol, self.devices_turn_on_codes.get(device_id).get("length"), None)
        self.rfdevice.cleanup()
"""

devices_turn_on_codes = {
            "1": {"code": 4265041, "length": 317},
            "3": {"code": 4264273, "length": 317},
            "4": {"code": 4261201, "length": 317},
            "5": {"code": 1381719, "length": 356}
        }

devices_turn_off_codes = {
            "1": {"code": 4265044, "length": 317},
            "3": {"code": 4264276, "length": 317},
            "4": {"code": 4261204, "length": 317},
            "5": {"code": 1381716, "length": 356}
        }

def turn_off(device_id):
    protocol = 1
    rfdevice = RFDevice(17)
    rfdevice.enable_tx()
    rfdevice.tx_repeat = 10
    rfdevice.tx_code(devices_turn_off_codes.get(device_id).get("code"), protocol,devices_turn_off_codes.get(device_id).get("length"), None)
    rfdevice.cleanup()

def turn_on(device_id):
    protocol = 1
    rfdevice = RFDevice(17)
    rfdevice.enable_tx()
    rfdevice.tx_repeat = 10
    rfdevice.tx_code(devices_turn_on_codes.get(device_id).get("code"), protocol,devices_turn_on_codes.get(device_id).get("length"), None)
    rfdevice.cleanup()