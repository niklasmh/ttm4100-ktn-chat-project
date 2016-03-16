#!Python27
# -*- coding: utf-8 -*-
import SocketServer
import json
import sys
import re
import random


# To save clients
clients = set()

# To save history
history = {}
history = json.loads("log.txt")

HOST, PORT = '0.0.0.0', 8888

class ClientHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.client = (self, "")
        
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
    allow_reuse_address = True

if __name__ == "__main__":
    print 'Server running...'
    server = ThreadedTCPServer((HOST, int(sys.argv[1] if len(sys.argv) > 1 else PORT)), ClientHandler)
    server.serve_forever()
