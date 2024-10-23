import client

def run_client(c: client.Client):
    while True:
        action = input("Enter 'login' or 'register': ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        request = client.Request('login', {'action': action, 'username': username, 'password': password})
        c.send(request)
        response = c.receive()
        if response.content['status'] == 'success':
            print("Success!")
            break
        else:
            print("Failure!")
            break

    c.close()

if __name__ == '__main__':
    c = client.Client()
    run_client(c)