#!Python27
# -*- coding: utf-8 -*-
import SocketServer
import json
#files to be used
#history saved in json object format (or compatible) user, time, message

HOST, PORT = '0.0.0.0', 8888

class ClientHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        
        while True:
            received_string = self.connection.recv(4096)
            
            if received_string:
                self.connection.send("ip: "
                                     + self.ip
                                     + " - "
                                     + received_string)
                received_object = json.decode(received_string);
                
                print "Message from: " + self.ip
                print "Request: " + received_string.request
                print "Message: " + received_string.content
                print "\n"


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    print 'Server running...'
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
