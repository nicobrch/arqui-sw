import socket
from dataclasses import dataclass

@dataclass
class Message():
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
class Service:
    name: str
    sock: socket.socket = None
    init: bool = False

    def sinit(self):
        if self.sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('soabus', 5000)
        print('starting up on {} port {}'.format(*server_address))
        try:
            self.sock.connect(server_address)
            self.send('sinit', self.name)
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
            msg = Message(content.decode(encoding="utf-8"))
            return msg
        except socket.error as e:
            print(f'socket error during receive: {e}')
            self.sock = None
            return ""
    
    def send(self, addr: str, content: str):
        if self.sock is None:
            raise ValueError("Socket is not initialized.")
        
        message = f'{len(addr+content):05}{addr}{content}'.encode()
        print('sending {!r}'.format(message))
        try:
            self.sock.sendall(message)
        except socket.error as e:
            print(f'socket error during send: {e}')
            self.sock = None

    def close(self):
        if self.sock:
            print('closing socket')
            self.sock.close()
            self.sock = None