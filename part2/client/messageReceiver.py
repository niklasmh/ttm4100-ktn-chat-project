#!Python27
# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    
    def __init__(self, client, connection):
        Thread.__init__(self)
        self.listener = client
        self.connection = connection
        self.daemon = True
    
    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while True:
            content = self.connection.recv(4096).decode("UTF-8")
            
            if content:
                self.listener.receive_message(content)
