
import socket
import asyncio
# Import smtplib for the actual sending function
import smtplib

class Taddle(object):

    def __init__(self,email,user,password):
        self.email = email 
        self.previous_ip = None
        # create the smtp daemon
        self.smtp = self.setup_smtp(user,password)

    def setup_smtp(self,user,password):
        print('Setting up smtp server...',end='')
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(
            user,
            password
        )
        print('done')
        return server 

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

    @property
    def hostname(self):
        return socket.gethostname()

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
        # Import the email modules we'll need
        from email.mime.text import MIMEText
        # Create a text/plain message
        msg = MIMEText("The IP address for {} is currently:{}".format(
            self.hostname,
            self.ip
            
        ))

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = 'IP update on {}'.format(self.hostname)
        msg['From'] = 'taddle@linkage.io'
        msg['To'] = self.email

        # Send the message via our own SMTP server.
        self.smtp.send_message(msg)
        # self.smtp.quit() 

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
        
