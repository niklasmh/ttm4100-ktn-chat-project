#!Python27
# -*- coding: utf-8 -*-
import socket
import json
from messageReceiver import MessageReceiver
from messageParser import MessageParser

host = "192.168.0.193"
port = 8888;

class Client:
    
    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
        
        self.host = host
        self.server_port = port
        
        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
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
        # Initiate the connection to the server
        print "Starting receiverThread..."
        self.start(self.host, self.server_port)
        print "receiverThread created!"
        
        while True:
            
            input = raw_input("Enter command: \n>> ")
            splitInput = input.split(" ", 1)
            print splitInput
            self.connection.send(self.send_payload(splitInput))
            
            while True:
                received_string = self.connection.recv(4096)
                
                if len(received_string[8:]) > 0:
                    print "Mottok:" + str(received_string)
                    break
                
            
            if raw_input("Exit chat? (y/n) \n>> ") == "y":
                break

    '''def disconnect(self):
        # TODO: Handle disconnection
        pass
    '''
    
    def receive_message(self, message):
        print message
        # TODO: Handle incoming message
        pass
    
    def send_payload(self, data):
        req = data[0]
        
        if len(data) == 2:
            content = data[1]
        else:
            content = None
        
        payload = { 'request': req, 'content': content }
        payload_as_string = json.dumps(payload)
        print payload_as_string
        
        return payload_as_string
        
        # TODO: Handle sending of a payload
    
    
    # More methods may be needed!


if __name__ == '__main__':
    client = Client(host, port)
