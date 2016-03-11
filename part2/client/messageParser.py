#!Python27

class MessageParser():
    def __init__(self):
        
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'login': self.parse_login, #ting Alex tror skal med herfra og ned
            'logout': self.parse_logout,
            'names': self.parse_names,
            'help': self.parse_help,
            'history': self.parse_history,
            'message': self.parse_message
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        #payload = # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            parse_error(payload)
            # Response not valid

    

    def parse_error(self, payload):
        return payload
    def parse_info(self, payload):
        return payload
    def parse_login(self, payload):
        return payload
    def parse_logout(self, payload):
        return payload
    def parse_names(self, payload):
        return payload
    def parse_help(self, payload):
        return payload
    def parse_history(self ,payload):
        return payload
    def parse_message(self, payload):
        return payload
    # Include more methods for handling the different responses... 

