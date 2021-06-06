import os
import sys
import json
from threading import Thread

from esptool import _main


class FlashOnce:
    def __init__(self):

        try:
            with open('config.json') as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            raise FileNotFoundError("The config.json file is missing in this directory")

        port = None
        try:
            port = sys.argv[1]
        except IndexError:
            raise ValueError(self.colored(200, 30, 30, "No COM Port Specified"))

        # Set the system arguments that the esptool will be using
        sys.argv = [
            __file__,
            "--port", port,
            # "--after", "no_reset",
            "write_flash", "0x00000", self.config["bin_file"],
            "--erase-all"
        ]

        self.esp_array = []
        self.device = None

    def run(self):
        flashing = Thread(target=_main, args=(self.esp_array,))
        flashing.start()
        flashing.join()

        try:
            self.device = self.esp_array[0]
        except IndexError:
            raise ValueError(self.colored(200, 30, 30, "No Device was returned by esptool.py _main"))

    def colored(self, r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

    def get_mac(self):
        return '%s' % (':'.join(map(lambda x: '%02x' % x, self.device.MAC_ADDRESS)))

    def save_to_file(self, add_to_existing=True):
        device_data = {
            self.device._port.port: {
                "NAME": f"{self.config['friendly_name']}_{self.get_mac().replace(':', '')[-6:].upper()}",
                "MAC": self.get_mac(),
            }
        }

        DEVICES = {}
        if os.path.exists("flashed.devices.json"):
            with open("flashed.devices.json", "r") as read_flashed_file:
                if os.stat("flashed.devices.json").st_size > 0:
                    DEVICES = json.load(read_flashed_file)
                DEVICES.update(device_data)

        with open("flashed.devices.json", "w") as write_flashed_file:
            write_flashed_file.write(
                json.dumps(DEVICES, indent=4)
            )


if __name__ == '__main__':
    flasher = FlashOnce()
    flasher.run()
    # flasher.save_to_file()

    print(flasher.colored(75, 181, 67, f"Finished Flashing device on com port: {flasher.device._port.port}"))
