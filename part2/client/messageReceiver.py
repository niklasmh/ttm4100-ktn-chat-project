#!Python27
# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):

    def __init__(self, client, connection):
        
        # Flag to run thread as a deamon
        #self.daemon = True
        
        self.listener = client
        self.connection = connection
        
        # TODO: Finish initialization of MessageReceiver
        #Thread.__init__(self)
        super(MessageReceiver, self).__init__()

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while True:
            content = self.connection.recv(4096)
            
            if len(content) > 0:
                self.listener.receive_message(content)
