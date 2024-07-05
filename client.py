import socket
from dataclasses import dataclass

@dataclass
class Message:
    msg: str
    addr: str = ""
    status: str = ""
    content: str = ""
    key: str = ""
    
    def __post_init__(self):
        self.addr = self.msg[:5]
        self.status = self.msg[5:7]
        if len(self.msg) >= 10 and self.msg[10] == "-":
            self.key = self.msg[7:10]
            self.content = self.msg[11:]
        else:
            self.content = self.msg[7:]

@dataclass
class Client:
    sock: socket.socket = None

    def connect(self):
        if self.sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        bus_address = ('localhost', 5000)
        print('connecting to {} port {}'.format(*bus_address))
        try:
            self.sock.connect(bus_address)
        except socket.error as e:
            print(f'socket error during initialization: {e}')
            self.sock = None

    def receive(self):
        if self.sock is None:
            raise ValueError("Socket is not initialized.")
        
        amount_received = 0
        try:
            amount_expected = int(self.sock.recv(5))
            while amount_received < amount_expected:
                content = self.sock.recv(amount_expected - amount_received)
                amount_received += len (content)
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