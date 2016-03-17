#!Python27
# -*- coding: utf-8 -*-
import SocketServer
import json
import sys
import re
import random
import time
from datetime import datetime

# To save clients
clients = set()

# To save history
history = []
history = json.loads(open('log.json', 'r').read())

HOST, PORT = '0.0.0.0', 8888

def output_format(name, content, response="message"):
    return {
                'timestamp': datetime.now().strftime("%m/%d - %H:%M:%S"),
                'name': name or 'Server',
                'response': response,
                'content' : content or ''
            }

def output_format_string(name, content, response="message"):
    return json.dumps(output_format(name, content, response), indent=4, sort_keys=True)

def add_log(name, content, response="message"):
    history.append(output_format(name, content, response))
    
    with open('log.json', 'w') as f:
         json.dump(history, f)

def get_log():
    return output_format_string("Server", json.dumps(json.loads(open('log.json', 'r').read()), indent=4, sort_keys=True), "history")

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
                
                if re.search(r'^\\?$|^[hi]$|^hj?elp$|^info$', request, re.I):
                        self.client[0].connection.send(output_format_string(self.client[1], "Hjelp:\n history/historie/log - Her får du opp historien.\n bye/exit/logout - Du vil bli logget ut.\n msg/message/'' - Dette vil sende en melding til alle andre som er logget på serveren.", "help"))
                elif self.client in clients:
                    
                    if re.search(r'^bye$|^exit$|^logout$', request, re.I):
                        self.client[0].connection.send(output_format_string(self.client[1], "Du ble logget ut", "logout"))
                        clients.remove(self.client)
                        
                        for c in clients:
                            
                            if c[0] != self:
                                c[0].connection.send(output_format_string(self.client[1], ": ble logget ut", "logout"))
                        
                    elif re.search(r'^log$|^history$|^historie$', request, re.I):
                        self.client[0].connection.send(get_log())
                    elif re.search(r'^names$|^navn$', request, re.I):
                        self.client[0].connection.send(output_format_string(self.client[1], "Navn: " + ", ".join([i[1] for i in clients]), "names"))
                    else:
                        msg = ""
                        
                        if not re.search(r'^msg|^message', request, re.I):
                            msg += request + " "
                        
                        msg += content
                        for c in clients:
                            if c[0] != self:
                                c[0].connection.send(output_format_string(self.client[1], msg, "message"))
                        
                        add_log(self.client[1], msg)
                else:
                    if request == "login":
                        
                        if content:
                            content = fix_string(content)
                        
                        taken = False
                        for i in clients:
                            if i[1] == content:
                                taken = True
                        
                        if taken:
                            self.client[0].connection.send(output_format_string(self.client[1], "Brukernavn tatt", "error"))
                            
                        else:
                            self.client = (self, content or "Guest" + str(random.randrange(1000, 9999, 1)))
                            clients.add(self.client)
                            self.client[0].connection.send(output_format_string(self.client[1], "Du ble logget inn som " + self.client[1], "login"))
                            
                            for c in clients:
                                if c[0] != self:
                                    c[0].connection.send(output_format_string(self.client[1], ": logget inn\n>> ", "login"))
                            
                            self.client[0].connection.send(get_log())
                    else:
                        self.client[0].connection.send(output_format_string("Anonym", "Du må logge inn. Se hjelp for mer info...", "error"))

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    print 'Server running...'
    server = ThreadedTCPServer((HOST, int(sys.argv[1] if len(sys.argv) > 1 else PORT)), ClientHandler)
    server.serve_forever()
