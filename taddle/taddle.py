
import socket
import asyncio

class Taddle(object):

    def __init__(self,email):
        self.email = email 


    @property
    def ip(self):
        '''
            get the IP from the current running machine
        '''
        return [l for l in ( \
            [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], \
            [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], \
            s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]] \
        ) if l][0][0]

    @asyncio.coroutine
    def watch_ip(self):
        print("current ip: {}".format(self.ip))

    @asyncio.coroutine
    def watch_nothing(self):
        print("This does nothing")
        

    @asyncio.coroutine
    def watch(self):
        yield from asyncio.sleep(5)
        asyncio.async(self.watch_ip())
        asyncio.async(self.watch_nothing())
        asyncio.async(self.watch())

    def run(self):
        ''' 
            If the current IP changes, then report them
        '''
        try:
            loop = asyncio.get_event_loop()
            asyncio.async(self.watch())
            loop.run_forever()
        finally:
            loop.close()
        
