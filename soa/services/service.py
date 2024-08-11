import socket
from dataclasses import dataclass

@dataclass
class Request():
    msg: str
    addr: str = ""
    content: str = ""
    key: str = ""

    def __post_init__(self):
        self.addr = self.msg[:5]
        if len(self.msg) >= 8 and self.msg[8] == "-":
            self.key = self.msg[5:8]
            self.content = self.msg[9:]
        else:
            self.content = self.msg[5:]

@dataclass
class Response():
    addr: str
    key: str
    content: str
    msg: bytes = b''

    def __post_init__(self):
        if self.key == '':
            length = len(self.addr + self.content)
            self.msg = f'{length:05}{self.addr}{self.content}'.encode()
        else:
            length = len(self.addr + self.content + self.key + '-') 
            self.msg = f'{length:05}{self.addr}{self.key}-{self.content}'.encode()

@dataclass
class Service:
    name: str
    sock: socket.socket = None
    init: bool = False

    def sinit(self):
        if self.sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('starting up on {} port {}'.format(*server_address))
        try:
            self.sock.connect(server_address)
            rs = Response('sinit', '', self.name)
            self.send(rs)
            self.receive()
            self.init = True
        except socket.error as e:
            print(f'socket error during initialization: {e}')
            self.sock = None

    def receive(self):
        if self.sock is None:
            raise ValueError("Socket is not initialized.")
        
        print ("Waiting for transaction")
        amount_received = 0
        try:
            amount_expected = int(self.sock.recv(5))
            while amount_received < amount_expected:
                content = self.sock.recv(amount_expected - amount_received)
                amount_received += len (content)
                print('received {!r}'.format(content))
            request = Request(msg=content.decode(encoding="utf-8"))
            return request
        except socket.error as e:
            print(f'socket error during receive: {e}')
            self.sock = None
            return ""
    
    def send(self, response: Response):
        if self.sock is None:
            raise ValueError("Socket is not initialized.")
        
        print('sending {!r}'.format(response.msg))
        try:
            self.sock.sendall(response.msg)
        except socket.error as e:
            print(f'socket error during send: {e}')
            self.sock = None

    def close(self):
        if self.sock:
            print('closing socket')
            self.sock.close()
            self.sock = None