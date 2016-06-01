
import socket
import asyncio

class Taddle(object):

    def __init__(self,email,user,password):
        self.email = email 
        self.previous_ip = None
        self.user = user
        self.password = password


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
        if self.ip != self.previous_ip:
            self.send_email() 
        self.previous_ip = self.ip

    @asyncio.coroutine
    def watch_nothing(self):
        print("This does nothing")
        

    @asyncio.coroutine
    def watch(self):
        yield from asyncio.sleep(300)
        asyncio.async(self.watch_ip())
        asyncio.async(self.watch_nothing())
        asyncio.async(self.watch())

    def send_email(self):
        # Import smtplib for the actual sending function
        import smtplib
        # Import the email modules we'll need
        from email.mime.text import MIMEText
        # Create a text/plain message
        msg = MIMEText("The IP address for Rapidash is currently:{}".format(self.ip))

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = 'IP update on Rapidash'
        msg['From'] = 'taddle@linkage.io'
        msg['To'] = self.email

        # Send the message via our own SMTP server.
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login(
            self.user,
            self.password
        )
        s.send_message(msg)
        s.quit() 

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
        
