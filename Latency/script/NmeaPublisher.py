#!/usr/bin/env python3

import socket
from datetime import datetime, timezone

import rospy

rospy
from dynamic_reconfigure.server import Server
from nmea_publisher.cfg import NmeaConfig

class NmeaPublisher:
    def __init__(self, address, port):  
        self.address = address
        self.port = port
        self.opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __del__(self):
        self.opened_socket.close()

    def getCurrentNmea(self):
        current_time = datetime.now(timezone.utc).strftime("%H%M%S.%f")[:-4]
        current_date = datetime.now().strftime("%d%m%y")

        nmea = f"$GPRMC,{current_time},A,4952.564827,N,00839.531926,E,0.00,0.00,{current_date},0.00,E,D,V*" # only that here config bzw date and time bekommen
        checksum = 0
        for b in nmea.encode("utf-8")[1:-1]:
            checksum = checksum ^ b
        return nmea + hex(checksum)[2:].upper() + "\r\n"

    def sendNmea(self):
        byte_message = bytes(self.getCurrentNmea(), "utf-8")
        try:
            self.opened_socket.sendto(byte_message, (self.address, self.port))
        except socket.error as exc:
            rospy.logfatal_throttle(5, f"UDP send error: {exc}\t Address: {self.address} Port: {self.port}")

    def setConfig(self, conf):
        self.address = conf["address"]
        self.port = conf["port"]


def reconfigureCallback(config, level):
    nmea.setConfig(config)
    rospy.loginfo(f'Reconfigure Request: Address: {config["address"]}, Port: {config["port"]}')
    return config


def run():
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        nmea.sendNmea()
        rate.sleep()

def initNode():
    global nmea
    nmea = NmeaPublisher("VLP11101190501138.oncar",  )
    rospy.init_node("NmeaPublisher", log_level=rospy.INFO)
    srv = Server(NmeaConfig, reconfigureCallback)

if __name__ == "__main__":
    initNode()
    try:
        run()
    except rospy.ROSInterruptException:
        pass
