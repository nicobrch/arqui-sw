import service
import db

def run_service(s: service.Service):
    usr = ""
    pwd = ""
    while True:
        data = s.receive()
        if type(data) != service.Message:
            print('Error en la transaccion!')
            continue
        
        if data.content == 'login':
            s.send('login', 'usr-> Ingrese su nombre de usuario:\n')
        elif data.key == "usr":
            usr = data.content
            s.send('login', 'pwd-> Ingrese su contrasena:\n')
        elif data.key == "pwd":
            pwd = data.content
            if db.verify_user(usr, pwd):
                s.send('login', 'scs-> Bienvenido, ' + usr + '!\n')
            else:
                s.send('login', 'err-> Usuario o contrasena incorrectos!\n')
        else:
            s.send('login', 'err-> Error en la transaccion!\n')

if __name__ == '__main__':
    s = service.Service('login')
    s.sinit()
    run_service(s)