#!Python27
# -*- coding: utf-8 -*-
import SocketServer
import json
import sys
#files to be used
#history saved in json object format (or compatible) user, time, message

# To save clients
clients = set()

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
                    for c in clients:
                        if c[0] != self:
                            c[0].connection.send("Melding fra " + self.client[1])
                    
                    print "Message from: " + self.ip
                    print "Request: " + request
                    print "Message: " + content
                    print "\n"
                    
                    if request == "logout":
                        clients.remove(self.client)
                else:
                    if request == "login":
                        self.client = (self, content or "")
                        clients.add(self.client)
                        
                        for c in clients:
                            if c[0] != self:
                                c[0].connection.send("Bruker: " + self.client[1] + " logget inn")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    print 'Server running...'
    server = ThreadedTCPServer((HOST, int(sys.argv[1] if len(sys.argv) > 1 else PORT)), ClientHandler)
    server.serve_forever()
