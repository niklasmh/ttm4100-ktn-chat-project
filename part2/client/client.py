#!Python27
# -*- coding: utf-8 -*-
import socket
import json
from messageReceiver import MessageReceiver
from messageParser import MessageParser
host = "78.91.13.83"
class Client:
    """
    This is the chat client class
    """
    host = "78.91.13.83"
    server_port = 8888

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code

        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        print "test"
        #self.connection.send("melding")
        
        
        while True:
            
            input = raw_input("Enter command")
            splitInput =  input.split(" ",1)
            print splitInput
            self.connection.send(self.send_payload(splitInput))
            
            while True:
                received_string = self.connection.recv(4096)
                if len(received_string[8:]) > 0:
                    print "Mottok:" + str(received_string)
                    break
                
        
            if raw_input("Exit chat?") == "y":
                break

    '''def disconnect(self):
        # TODO: Handle disconnection
        pass
        '''
    '''
    def receive_message(self, message):
        print message
        # TODO: Handle incoming message
        pass
    '''
    def send_payload(self, data):
        req = data[0]
        if len(data) == 2:
            content = data[1]
        else:
            content = None
        payload = {'request': req, 'content':content}
        payload_as_string = json.dumps(payload)
        print payload_as_string
        return payload_as_string                        
                                 
        
        # TODO: Handle sending of a payload
    
    
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client(host, 8888)
