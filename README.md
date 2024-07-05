# PySoa

Este proyecto es una implementación de SOA (Arquitectura Orientada a Servicios) para el ramo de Arquitectura de Software, utilizando python como lenguaje y el bus provisto por el profesor de la cátedra. El proyecto consiste de:

- Docker de bus de datos
- Docker de base de datos Postgres
- ORM de base de datos SQLAlchemy
- Cliente y servicios en Python
- Dockerización de los servicios

## Ejecución

Primero, hay que ejecutar los siguientes comandos para levantar cada uno de los dockers:

**1. Crear red externa**

```shell
docker network create shared_network
```

**2. Ejecutar bus de datos**

```shell
docker run -d --name soabus --network shared_network -p 5000:5000 jrgiadach/soabus
```

**3. Levantar BDD Postgres**

```shell
cd db
docker run -d --name postgres --network shared_network -p 5432:5432 pysoa-db
```

**4. Levantar servicios**

```shell
cd ..
docker compose up
```

**4. Instalar dependencias en entorno virtual**

```shell
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

## Ejemplo de Uso

Una vez realizado todos los pasos de la Ejecución, estará escuchando el servicio de prueba "login". Para probar esto, abre una terminal con el entorno virtual activado y ejecuta el comando `python clogin.py`. Esto abrirá la interfaz del cliente Login. Para probar que funciona correctamente, utiliza el usuario "admin" y contraseña "admin".

## Crear cliente y servicio propio

Puedes copiar los archivos `clogin.py` y `slogin.py`, que corresponden al cliente y servicio respectivamente.

### Cliente

El cliente importa el módulo client, para crear un nuevo cliente. Para comenzar la interacción con el servidor mediante el bus, debe enviar le mensaje "login" a la dirección "login", que es el nombre del servicio.

### Servicio

El servicio importa el módulo servicio, para crear un nuevo servicio dado un nombre de 5 carácteres. En primer lugar el servicio debe inicializarse con el bus, usando la función sinit. Luego se ejecuta la lógica del servicio dentro de un ciclo.

### Transacciones

Para las transacciones, se utiliza el formato establecido por el bus de datos, con la diferencia que en el campo de contenido, se utilizan los primeros 4 carácteres para identificar la acción a realizar como `data.key`. Por ejemplo, si el cliente envía "usr-Hola" al servicio login, significa que enviará el nombre de usuario "Hola". Luego, el servicio identifica si el `data.key` corresponde a "usr", si es así guarda el contenido "Hola" en una variable.