#!Python27
# -*- coding: utf-8 -*-
import SocketServer
#files to be used
#history saved in json object format (or compatible) user, time, message


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
        
        while True:
            received_string = self.connection.recv(4096)
            
            if len(received_string) > 0:
                self.connection.send("ip: " + self.ip + " - " + received_string)
                print "Message from: " + self.ip
                print "Message: " + received_string
                print "\n"


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 8888
    print 'Server running...'
    
    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
