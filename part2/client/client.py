#!Python27
# -*- coding: utf-8 -*-
import socket
import json
#from MessageReceiver import MessageReceiver
#from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """
    host = 'localhost'
    server_port = 9998

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
    
    '''def disconnect(self):
        # TODO: Handle disconnection
        pass
        '''
    
    def receive_message(self, message):
        print message
        # TODO: Handle incoming message
        pass
    '''
    def send_payload(self, data):
        # TODO: Handle sending of a payload
        pass
    '''
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
