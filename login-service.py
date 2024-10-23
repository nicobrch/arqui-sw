import service
import db

def run_service(s: service.Service):
    s.sinit()
    while True:
        request = s.receive()
        if request.content['action'] == 'login':
            username = request.content['username']
            password = request.content['password']
            if db.verify_password(username, password):
                response = service.Response(s.name, {'status': 'success'})
            else:
                response = service.Response(s.name, {'status': 'failure'})
            s.send(response)
        elif request.content['action'] == 'register':
            username = request.content['username']
            password = request.content['password']
            db.add_user(username, password)
            response = service.Response(s.name, {'status': 'success'})
            s.send(response)
        else:
            response = service.Response(s.name, {'status': 'failure'})
            s.send(response)
    s.close()

if __name__ == '__main__':
    s = service.Service('login')
    run_service(s)