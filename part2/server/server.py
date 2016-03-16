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
history = {
    "id": 10,
    "name": "noen"
}
#history = open('log.json', 'r').read()
print history
#print json.load('log.json')

HOST, PORT = '0.0.0.0', 8888

def fix_string(name):
    return re.sub(r'[^a-z0-9A-Z ]', '', name)

def fix_word(name):
    return re.sub(r'[^a-z0-9A-Z]', '', name)

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
                
                if re.search(r'^\?$|^help$', request, re.I):
                        self.client[0].connection.send("Hjelp:\n history/historie/log - Her får du opp historien.\n bye/exit/logout - Du vil bli logget ut.\n msg/message/'' - Dette vil sende en melding til alle andre som er logget på serveren.")
                elif self.client in clients:
                    
                    if re.search(r'^bye$|^exit$|^logout$', request, re.I):
                        self.client[0].connection.send("Du ble logget ut")
                        clients.remove(self.client)
                        
                        for c in clients:
                            
                            if c[0] != self:
                                c[0].connection.send(self.client[1] + ": ble logget ut")
                        
                    elif re.search(r'^log$|^history$|^historie$', request, re.I):
                        self.client[0].connection.send("Her skal det være historie")
                    else:
                        msg = ""
                        
                        if not re.search(r'^msg|^message', request, re.I):
                            msg += request + " "
                        
                        msg += content
                        for c in clients:
                            if c[0] != self:
                                c[0].connection.send(self.client[1] + ": " + msg + "\n>> ")
                else:
                    if request == "login":
                        
                        if content:
                            content = fix_string(content)
                        
                        self.client = (self, content or "Guest" + str(random.randrange(1000, 9999, 1)))
                        clients.add(self.client)
                        
                        for c in clients:
                            if c[0] != self:
                                c[0].connection.send(self.client[1] + ": logget inn\n>> ")
    
    def addToLog(msg, clientname):
        pass

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    print 'Server running...'
    server = ThreadedTCPServer((HOST, int(sys.argv[1] if len(sys.argv) > 1 else PORT)), ClientHandler)
    server.serve_forever()
