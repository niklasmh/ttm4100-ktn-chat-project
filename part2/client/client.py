#!Python27
# -*- coding: utf-8 -*-
import socket
import json
from time import sleep
from messageReceiver import MessageReceiver
from messageParser import MessageParser

host = "123.456.0.789"
port = 8888;
from connectionInfo import *

class Client:
    
    def __init__(self, host, server_port):
        self.host = host
        self.server_port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print "Kobler til server..."
        self.connection.connect((self.host, self.server_port))
        print "Kobling suksessfull"
        
        print "Kjører i gang..."
        self.run()
        print "Ferdig med run"
    
    def start(self, host, server_port):
        recieverThread = MessageReceiver(self, self.connection)
        recieverThread.daemon = True
        recieverThread.start()
        print "Thread name: ", recieverThread.name
    
    def run(self):
        print "Starting receiverThread..."
        self.start(self.host, self.server_port)
        print "receiverThread created!\nTrying to recieve some information from the databases at Pentagon and NASA..."
        sleep(.3)
        print "."
        sleep(.3)
        print ".."
        sleep(.3)
        print "..."
        sleep(.3)
        print "Information received. Success!"
        print "Initializing a new chat session..."
        
        while True:
            input = raw_input("Enter command: \n>> ")
            splitInput = input.split(" ", 1)
            jsonFormat = self.send_payload(splitInput)
            print jsonFormat
            self.connection.send(jsonFormat)
    
    def disconnect(self):
        self.connection.close()
        print "Connection closed"
    
    def receive_message(self, message):
        print message
    
    def send_payload(self, data):
        req = data[0]
        content = data[1] if len(data) > 1 else None
        
        payload = { 'request': req, 'content': content }
        payload_as_string = json.dumps(payload)
        print payload_as_string
        
        return payload_as_string

if __name__ == '__main__':
    client = Client(host, port)
