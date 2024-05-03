import sys
import serial
import requests
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List
from time import sleep
import argparse



@dataclass
class sensorSerial:
    sensor_longitude: float
    sensor_latitude: float
    sensor_histo_date: int
    sensor_histo_value: float


@dataclass
class sensorDB:
    sensor_id: int
    sensor_longitude: float
    sensor_latitude: float
    sensor_histo_date: str


ser = serial.Serial()


def init_gateway(argv, parameter) -> dict:
    print("init_gateway")
    for element in enumerate(argv):
        if element[1] == "-s":
            parameter["gateway-type"] = "server"
        if element[1] == "-c":
            parameter["gateway-type"] = "client"
        if element[1] == "-d":
            parameter["debug"] = True
        if element[1] == "-com":
            parameter["port-com"] = argv[element[0]+1]
        if element[1] == "-api":
            parameter["api-url"] = argv[element[0]+1]
        if element[1] == "-baudrate":
            parameter["baud-rate"] = int(argv[element[0]+1])

    return parameter


def init_uart() -> None:
    logging.debug("init_uart")
    ser.port = args.port_com
    ser.baudrate = args.baud_rate
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = None

    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False
    try:
        ser.open()
    except serial.SerialException as e:
        logging.error(f"{e}")
        sys.exit(1)


def send_uart_message(message) -> None:
    ser.flush()
    ser.write(message.encode())
    logging.debug(f"send_uart_message : {message}")


def debug_data() -> List[dict]:
    data_debug = []

    for i in range(1, 6):
        for j in range(1, 10):
            data_debug.append({
                "x": i,
                "y": j,
                "date": int(datetime.now().timestamp()),
                "level": 0
            })

    return data_debug


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gateway for sensor')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--gateway', action='store_true', help='Gateway mode')
    group.add_argument('-s', '--sensor', action='store_true', help='Sensor mode')
    parser.add_argument('-d', '--debug', action='store_true', help='Debug mode')
    parser.add_argument('-c', '--port-com', type=str, help='Port COM', default='COM3')
    parser.add_argument('-a', '--api-url', type=str, help='API URL', default='http://127.0.0.1:8080')
    parser.add_argument('-b', '--baud-rate', type=int, help='Baud Rate', default=115200)

    args = parser.parse_args()
    if args.debug:
        print("Debug Mode")
        logging.basicConfig(level=logging.DEBUG, encoding='utf-8', format='%(asctime)s %(levelname)s %(message)s')

        print(args)
    else:
        logging.basicConfig(level=logging.INFO, encoding='utf-8', format='%(asctime)s %(levelname)s %(message)s')

    init_uart()
    logging.debug("Debug on port " + args.port_com)

    if args.gateway:
        logging.debug("Gateway Mode")


        try:
            while ser.is_open:
                data_str = ser.readline()
                logging.debug(f"data received : {data_str} ")
                data_decode = data_str.decode('utf-8').split("}")
                if data_decode == "{init":
                	continue

                data_json = json.loads(data_decode[0]+"}")
                logging.debug(f"data json : {data_json}, type : {type(data_json)}")

                obj = sensorSerial(data_json["x"], data_json["y"], data_json["date"], data_json["level"])
                logging.debug(f"obj : {obj}")
                response = requests.get(args.api_rul+f"/api/v1/sensor/coordinates/{obj.sensor_longitude}/{obj.sensor_latitude}")
                if response.status_code == 404:
                    response = requests.post(args.api_url+f"/api/v1/sensor", json={

                        "sensor_longitude": obj.sensor_longitude,
                        "sensor_latitude": obj.sensor_latitude
                    })
                logging.debug(f"response : {response.json()['id_sensor']}")
                sensor_histo = requests.post(args.api_url+f"/api/v1/sensor-histo", json={

                    "id_sensor": response.json()["id_sensor"],
                    "sensor_histo_value": obj.sensor_histo_value,
                    "sensor_histo_date": datetime.fromtimestamp(obj.sensor_histo_date).strftime("%Y-%m-%d %H:%M:%S")

                })
        except (KeyboardInterrupt, SystemExit):
            ser.close()
            logging.info("Gateway Stopped")

    if args.sensor:
        logging.debug("Client Mode")
        data_client = []
        if args.debug:

            data_client = debug_data()
        init = "{init}"
        send_uart_message(init)
        toto = ser.read(len(init))
        c = ser.read(1)


        for element in data_client:
            data_to_send = '{"x": %d, "y": %d, "date": %d, "level": %d}' % (element["x"], element["y"], element["date"], element["level"])
            logging.debug(f"data to send : {data_to_send}")
            logging.debug("date: " + datetime.fromtimestamp(element["date"]).strftime("%Y-%m-%d %H:%M:%S"))
            send_uart_message(data_to_send)
            logging.debug("data len : " + str(len(data_to_send)))
            logging.debug(type(data_to_send))
            toto = ser.read(len(data_to_send))
            logging.debug(f"Serial Feed Back : {toto}")
            c = ser.read(1)

            logging.debug(c)











