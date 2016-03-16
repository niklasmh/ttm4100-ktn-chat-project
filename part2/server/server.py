#!Python27
# -*- coding: utf-8 -*-
import SocketServer
import json
import sys
import re
import random



"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            

            if received_string:
                print "Mottok:"
                print received_string
                
                received_object = json.loads(received_string)
                request = received_object['request'] or ""
                content = received_object['content'] or ""
                
                if self.client in clients:
                    
                    if re.search(r'^bye$|^exit$|^logout$', request, re.I):
                        self.client[0].connection.send("Du ble logget ut")
                        clients.remove(self.client)
                    elif re.search(r'^log$|^history$|^historie$', request, re.I):
                        self.client[0].connection.send("Her skal det være historie")
                    elif re.search(r'^\?$|^help$', request, re.I):
                        self.client[0].connection.send("Hjelp:\n history/historie/log - Her får du opp historien.\n bye/exit/logout - Du vil bli logget ut.\n msg/message/'' - Dette vil sende en melding til alle andre som er logget på serveren.")
                    else:
                        msg = ""
                        
                        if not re.search(r'^msg|^message', request, re.I):
                            msg += request + " "
                        
                        msg += content
                        for c in clients:
                            if c[0] != self:
                                c[0].connection.send("Melding fra "
                                                     + self.client[1] 
                                                     + ": "
                                                     + msg)
                else:
                    if request == "login":
                        if content:
                            content = re.sub(r'[^a-z0-9]', '', content)
                        self.client = (self, content or "Guest" + random.randrange(1000, 9999, 1))
                        clients.add(self.client)
                        
                        for c in clients:
                            if c[0] != self:
                                c[0].connection.send("Bruker: " + self.client[1] + " logget inn")
    
    def addToLog(msg, clientname):
        pass

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
