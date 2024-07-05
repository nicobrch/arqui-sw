import client

def run_client(c: client.Client):
    usr = ""
    pwd = ""

    while True:
        data = c.receive()
        if type(data) != client.Message:
            raise ValueError('Error en la transaccion!')

        if data.key == "usr":
            usr = input(data.content)
            c.send('login', f'usr-{usr}')
        elif data.key == "pwd":
            pwd = input(data.content)
            c.send('login', f'pwd-{pwd}')
        else:
            print(data.content)
            break

if __name__ == '__main__':
    c = client.Client()
    c.connect()
    c.send('login', 'login')
    run_client(c)