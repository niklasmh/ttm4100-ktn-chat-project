#!Python27
# -*- coding: utf-8 -*-
import socket
import json
import sys
import re
from time import sleep
from messageReceiver import MessageReceiver
from messageParser import MessageParser

HOST = "123.456.0.789"
PORT = 8888;
from connectionInfo import *

class Client:
    
    def __init__(self, host, server_port):
        self.host = host
        self.server_port = server_port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print "Kobler til server..."
        self.connection.connect((self.host, self.server_port))
        print "Kobling suksessfull"
        
        print "Kjører i gang..."
        self.run()
        print "Ferdig med run"
    
    def start(self, host, server_port):
        recieverThread = MessageReceiver(self, self.connection)
        recieverThread.start()
    
    def run(self):
        print "Starting receiverThread..."
        self.start(self.host, self.server_port)
        print "receiverThread created!\nTrying to recieve some information from the databases at Pentagon and NASA..."
        sleep(.1)
        print "."
        sleep(.1)
        print ".."
        sleep(.1)
        print "..."
        sleep(.1)
        print "Information received. Success!"
        print "Initializing a new chat session..."
        
        while 1:
            input = raw_input("\nEnter command: \n>> ")
            splitInput = input.split(" ", 1)
            jsonFormat = self.send_payload(splitInput)
            self.connection.send(jsonFormat)
            sleep(.1)
            
            if re.search(r'^bye$|^exit$|^logout$', splitInput[0], re.I):
                self.disconnect()
                
                if re.search(r'^bye$|^exit$', splitInput[0], re.I):
                    self.quit()
    
    def disconnect(self):
        self.connection.close()
        print "Connection closed"
    
    def quit(self):
        print "Bye"
        exit()
    
    def receive_message(self, message):
        print "\nServer: " + message + "\n>> ",
    
    def send_payload(self, data):
        req = data[0]
        content = data[1] if len(data) > 1 else None
        
        payload = { 'request': req, 'content': content }
        payload_as_string = json.dumps(payload)
        
        return payload_as_string

if __name__ == '__main__':
    client = Client(HOST, int(sys.argv[1] if len(sys.argv) > 1 else PORT))
