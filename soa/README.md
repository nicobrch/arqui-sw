# SOA

Esto es un ejemplo de implementación de SOA, con cliente y servicios para iniciar sesión en una base de datos SQLite. Para comunicarse, los clientes y servicios utilizan como intermediario el BUS, el cuál es ejecutado mediante docker y los comunica utilizando el protocolo TCP. 

## Explicación

Para crear los clientes y servicios, se crearon archivos genéricos llamados `"client.py"` y `"service.py"`. Utilizando programación orientada a objetos, cada uno de estos programas es enviar de enviar "Requests" y "Responses" al bus, con el siguiente formato:

* **Client Request / Service Response:** Es un mensaje que contiene una dirección (addr), una llave (key), un contenido (content) y un mensaje (msg). Esto significa que hay que indicar la dirección a la que se envía el mensaje (nombre del servicio), una llave para indicar etapas/lógica, un contenido que es el mensaje como tal del usuario, y finalmente el mensaje que es formateado automáticamente como bytes para enviar al bus.
* **Client Response / Service Request:** Es una petición que es enviadad esde el bus hacia los clientes/servicios. Este contiene un mensaje (msg, en bytes), una dirección, contenido y llave. Esto sirve para poder identificar fácilmente los campos y seguir la lógica de operación.

## Ejecución

1. Primero ejecutaremos los servicios y el bus, los cuáles serán comunicados mediante una red externa:

```bash
docker network create soa
```

2. Luego, ejecutamos el bus de datos provisto por el profesor (recomiendo esto en vez de ejecutarlo en el mismo docker compose, para el desarrollo):

```bash
docker run -d -p 5000:5000 --name soabus --network soa jrgiadach/soabus:v1
```

3. Posteriormente, ejecutamos los servicios creados usando docker compose:

```bash
# Debes estar en la carpeta /soa
docker compose up --build
```

4. Finalmente probamos el servicio utilizando el cliente respectivo en nuestra terminal:

```bash
# Debes estar en la carpeta /soa/clients
python login.py
```

Si todo funcionó correctamente, prueba ingresar el usuario "nico" y la contraseña "123123".