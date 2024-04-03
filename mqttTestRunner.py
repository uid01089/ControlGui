import logging
import time

import paho.mqtt.client as pahoMqtt

from PythonLib.Mqtt import Mqtt


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('ChargeControl').setLevel(logging.DEBUG)

    mqttClient = Mqtt("koserver.iot", "/test", pahoMqtt.Client("Testrunner"))
    ctr = 0

    while (True):

        mqttClient.publish("ctr", str(ctr))
        ctr = ctr + 1
        time.sleep(1.0)


if __name__ == '__main__':
    main()
