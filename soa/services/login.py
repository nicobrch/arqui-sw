import service
import db

def run_service(s: service.Service):
    usr = ""
    pwd = ""
    while True:
        data = s.receive()
        if type(data) != service.Request:
            print('Error en la transaccion!')
            continue
        
        if data.key == 'ini':
            rs = service.Response('login', 'usr', '> Ingrese su nombre de usuario:\n')
            s.send(rs)
        elif data.key == "usr":
            usr = data.content
            rs = service.Response('login', 'pwd', '> Ingrese su contrasena:\n')
            s.send(rs)
        elif data.key == "pwd":
            pwd = data.content
            if db.verify_password(usr, pwd):
                rs = service.Response('login', 'oks', '> Bienvenido!\n')
                s.send(rs)
                break
            else:
                rs = service.Response('login', 'err', '> Contrasena incorrecta!\n')
                s.send(rs)
        else:
            rs = service.Response('login', 'err', '> Error en la transaccion!\n')
            s.send(rs)
    
    s.close()

if __name__ == '__main__':
    s = service.Service('login')
    s.sinit()
    run_service(s)