#!Python27
import re

class MessageParser():
    
    def __init__(self):
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'login': self.parse_login,
            'logout': self.parse_logout,
            'names': self.parse_names,
            'help': self.parse_help,
            'history': self.parse_history,
            'message': self.parse_message
        }
    
    def parse(self, payload):
        
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            self.parse_error(payload)
    
    def parse_error(self, payload):
        print self.format_payload(payload, formatted="%timestamp% Error: %content%")
    
    def parse_info(self, payload):
        print self.format_payload(payload, formatted="%timestamp% Info: %content%")
    
    def parse_login(self, payload):
        print self.format_payload(payload, formatted="%timestamp%: %name% logget inn")
    
    def parse_logout(self, payload):
        print self.format_payload(payload, formatted="%timestamp%: %name% ble logget ut")
    
    def parse_names(self, payload):
        print self.format_payload(payload, formatted="\nListe med navn i chatten:\n%content%\n")
    
    def parse_help(self, payload):
        print self.format_payload(payload, formatted="%timestamp%\n\n%content%\n")
    
    def parse_history(self ,payload):
        print self.format_payload(payload)
    
    def parse_message(self, payload):
        print self.format_payload(payload)
    
    # Creates a message in current format
    def format_payload(self, payload, formatted="%timestamp% %name%: %content%"):
        for i in payload:
            formatted = re.sub(r'%' + i + '%', payload[i], formatted)
        
        return formatted
