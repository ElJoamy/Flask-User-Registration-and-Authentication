# Proyecto de Registro de Usuarios con Flask y MongoDB

Este proyecto es una aplicación web de registro de usuarios desarrollada en Python con Flask y MongoDB, empaquetada en un contenedor Docker. La aplicación permite a los usuarios registrarse, iniciar sesión y actualizar su información de perfil. A continuación, se proporciona una guía completa sobre cómo configurar y ejecutar la aplicación.

## Estructura del Proyecto

La estructura del proyecto es la siguiente:

- **docker-compose.yml**: Define los servicios necesarios para ejecutar la aplicación, incluyendo la aplicación Flask y una instancia de MongoDB.

- **Dockerfile**: Se utiliza para construir una imagen Docker de la aplicación Flask.

- **app**: Carpeta que contiene el código de la aplicación Flask, incluyendo rutas para registro, inicio de sesión, actualización de usuarios y otras funciones auxiliares.

- **paises.csv**: Un archivo CSV que contiene información sobre códigos de países.

- **.env.example**: Un archivo de ejemplo que contiene variables de entorno necesarias para la aplicación. Debe renombrarse a `.env` y configurarse con valores adecuados antes de ejecutar la aplicación.

- **templates**: Carpeta que contiene las plantillas HTML para las páginas de inicio, registro y inicio de sesión.

- **uploads**: Carpeta donde se almacenan las imágenes de perfil de los usuarios.

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instalado Docker y Docker Compose en tu sistema. Puedes instalarlos siguiendo las instrucciones en el sitio web oficial de Docker:

- Docker y Docker Compose: [Instalación de Docker](https://docs.docker.com/engine/install/debian/)

## Cómo Ejecutar la Aplicación

Siga estos pasos para ejecutar la aplicación en su entorno local:

1. Clone el repositorio a su sistema:

    ```bash
    git clone https://tu-repositorio.git
    ```

2. Acceda al directorio del proyecto:

    ```bash
    cd nombre-de-tu-proyecto
    ```

3. Cree un archivo `.env` basado en el archivo `.env.example` proporcionado y configure las variables de entorno necesarias. Las variables de entorno definidas en `.env` son esenciales para el funcionamiento de la aplicación. Asegúrese de configurarlas correctamente. Aquí hay un ejemplo de configuración para el archivo `.env`:

    ```env
    RUTA_CSV_PAISES=paises.csv
    UPLOAD_FOLDER=uploads/
    ```

    Asegúrese de que `RUTA_CSV_PAISES` apunte al archivo `paises.csv` en el directorio raíz del proyecto.

4. En el archivo `docker-compose.yml`, asegurese de cambair lo siguiente:

    ```yml
        parent: ens33 # Reemplaza esto con el nombre de la interfaz del host que deseas utilizar

        - subnet: <tu_subnet_elegido>  # Reemplaza esto con tu subnet deseado, p. ej., "192.168.1.0/24"
        - gateway: <tu_gateway_elegido>  # Reemplaza esto con tu gateway deseado, p. ej., "192.168.1.2
    ```

5. Ejecute el siguiente comando en la raíz del proyecto para iniciar la aplicación:

    ```bash
    docker-compose up --build
    ```

6. La aplicación estará disponible en `http://localhost:5000` en su navegador.

## Funcionalidades de la Aplicación

La aplicación web de registro de usuarios ofrece las siguientes funcionalidades:

### Registro de Usuarios

- Los usuarios pueden registrarse proporcionando su dirección de correo electrónico, nombre de usuario, contraseña y otros datos opcionales.

- La aplicación valida la dirección de correo electrónico, verifica si la contraseña cumple con ciertos criterios y verifica si el código de país (opcional) es válido.

- Los usuarios pueden cargar una imagen de perfil que se almacena en la carpeta `uploads/`.

- La contraseña se almacena de manera segura como un hash en la base de datos MongoDB.

### Inicio de Sesión

- Los usuarios pueden iniciar sesión utilizando su nombre de usuario o dirección de correo electrónico y su contraseña.

- La aplicación valida las credenciales y autentica a los usuarios.

### Actualización de Perfil

- Los usuarios autenticados pueden actualizar su perfil, incluyendo su nombre de usuario, dirección de correo electrónico, contraseña, imagen de perfil y otros datos personales.

- La aplicación valida y procesa las actualizaciones de perfil de manera segura.

### Consulta de Usuarios

- La aplicación permite consultar la lista de usuarios registrados en la base de datos.

- Los datos de los usuarios se almacenan en una base de datos MongoDB.

### Eliminación de Usuarios

- Los administradores pueden eliminar usuarios de la base de datos.

## Personalización de la Plantilla

Las plantillas HTML en la carpeta `templates` pueden personalizarse según las necesidades de diseño y marca de su proyecto. Puede modificar el aspecto y la estructura de las páginas de inicio, registro e inicio de sesión.

## Consideraciones Importantes

- Asegúrese de que el servicio MongoDB se encuentre en ejecución antes de iniciar la aplicación Flask. Docker Compose se encarga de crear una red para la comunicación entre ambos servicios.

- Los usuarios registrados se almacenan en una base de datos MongoDB. Puede acceder a la base de datos MongoDB desde la aplicación Flask utilizando la biblioteca `pymongo`.

