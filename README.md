# SOA

Esto es un ejemplo de implementación de SOA, con cliente y servicios para iniciar sesión en una base de datos SQLite. Para comunicarse, los clientes y servicios utilizan como intermediario el BUS, el cuál es ejecutado en un contenedor docker y los comunica utilizando el protocolo TCP.

## Video Demostración

Pueden ver la demostración y explicación de este repo aquí: [Video Demostración](https://youtu.be/lJ2WTdn6lVs)

## Ejecución

Deben ejecutar el contenedor del BUS, con el siguiente comando:

```bash
docker run -d -p 5000:5000 --name soabus jrgiadach/soabus:v1
```

(Opcional) Si planean ejecutar sus servicios en contenedores también, les recomiendo crear una network para así poder conectarlos facilmente con el docker, de la siguiente forma:

```bash
docket network create soa
```

```bash
docker run -d -p 5000:5000 --name soabus --network soa jrgiadach/soabus:v1
```

Si lo hacen de esta manera, deben modificar el host de sus servicios, para que en vez de conectarse a localhost se conecten a `bus:5000`. Utilizando el código de este repo, pueden crear un archivo `.env` con la variable `HOST=bus`.

Luego, sólo deben ejecutar sus servicios. Si lo hicieron en python como en este repo, pueden abrir una terminal para cada uno y ejecutarlos con el comando `python servicio.py`. Idealmente si tienen muchos servicios, creen un docker-compose para ejecutarlos todos desde una misma terminal.

## Explicación del Código

### Nomenclatura BUS

El bus recibe strings, en formato de bytes, con la siguiente nomenclatura:

NNNNNSSSSSDDDDD

Los primeros 5 carácteres (NNNNN) indican el largo del mensaje, sin incluirse a si mismo. Si el mensaje es de 100 carácteres, entonces NNNNN será 00100.

Luego, los siguientes 5 carácteres (SSSSS) indican el nombre del servicio. Para que funcione esto, los servicios deben estar inicializados previamente.

Finalmente, se envían los datos (DDDDD). Esto no tiene una cantidad definida de carácteres, pero debe ser menor a 99999, que es el largo máximo de carácteres que permite el bus.

Para responder, el bus utiliza la misma nomenclatura, con una pequeña diferencia:

NNNNNSSSSSTTDDDDD

Entre el nombre del servicio y los datos, se agregan 2 carácteres (TT). Esto indica el estado de la comunicación. Si la comunicación fue efectiva, TT es un OK, si hubo algún error en la comunicación, TT es NK.

### Servicios

Primero, se deben diseñar los servicios. El código de este repo provee un archivo `service.py`, el cuál define una clase genérica para instanciar servicios.

1. Primero, se debe inicializar, enviando un mensaje `00010sinitlogin` al bus, donde sinit es el código clave para inicializar un servicio, y login es el nombre de este servicio.

2. Luego, se recibe la respuesta del BUS, y si esta fue efectiva, se comienza a operar. 

3. La clase servicio está diseñada para trabajar con objetos de tipo llave-valor. Se asume que el contenido del mensaje es un objeto, y se obtienen los valores correspondientes para su operación.

4. Finalmente, una vez realizada la lógica y procesamiento, envía una respuesta con el mismo formato de objeto llave-valor, que es recibida por el cliente.

### Clientes

Los clientes utilizan la misma estructura, donde existe una clase genérica `client.py` para crear clientes.

1. Se inicializa el cliente, que simplemente se conecta al bus en `host:5000`.

2. Luego, se hace la lógica respecto al cliente. En el caso del login, se solicita un usuario y contraseña por teclado, junto al tipo de login que se desea realizar.

3. El cliente envía una request con formato objeto llave-valor, donde se indica primeramente el nombre del servicio a realizar la request, seguido del contenido (el objeto llave-valor). 

4. Finalmente, el cliente espera la respuesta del bus (que está dada por el servicio) y desplega el resultado.