import client

def run_client(c: client.Client):
    usr = ""
    pwd = ""

    while True:
        data = c.receive()
        if type(data) != client.Response:
            raise ValueError('Error en la transaccion!')

        if data.key == "usr":
            usr = input(data.content)
            rq = client.Request('login', 'usr', usr)
            c.send(rq)
        elif data.key == "pwd":
            pwd = input(data.content)
            rq = client.Request('login', 'pwd', pwd)
            c.send(rq)
        else:
            print(data.content)
            break

if __name__ == '__main__':
    c = client.Client()
    c.connect()
    rq = client.Request('login', 'ini', '')
    c.send(rq)
    run_client(c)