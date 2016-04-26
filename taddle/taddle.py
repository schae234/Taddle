
import socket

class Taddle(object):

    def __init__(self,email):
        self.ip = self.get_ip()
        self.email = email 


    def get_ip(self):
        '''
            get the IP from the current running machine
        '''
        [l for l in ( \
            [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], \
            [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], \
            s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]] \
        ) if l][0][0]
        self.email = email


    def watch_ip(self):
        ''' 
            If the current IP changes, then report to the email
        '''
        loop = asyncio.get_event_loop()
        
