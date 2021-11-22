# Tutorial para uso de EEG

## Instalación de paquetes y librerías

Antes del uso normal del sistema se requiere tener instalado en Windows "Python", para verificar la instalación puede presionar inicio en la parte inferior izquierda de su pantalla y escribir "Python" (no es necesario presionar algo más, solo de click en inicio y escriba sin seleccionar nada, el sistema operativo buscará automáticamente).

En caso que no esté instalado puede instalarlo desde:

https://www.python.org/downloads/release/python-2718/

Solo debe descargar el archivo "Windows x86-64 MSI installer" para los dispositivos con windows 64bits o en caso contrario "Windows x86 MSI installer" para los de 32bits y seguir los pasos de instalación, asegurandose que al final se agregue python al "PATH de Windows".

En caso de no hacerlo directamente se debe agregar al path de manera manual para poder ser usado en la ventana de comandos, para hacer esto vamos a inicio y buscamos "variables de entorno", esto nos permitirá abrir las "propiedades del sistema", en la pestaña de opciones avanzadas, debemos presionar el último botón debajo de todo que dice "variables de entorno...", luego, en el apartado de "Variables del sistema" debemos buscar y hacer doble click en la variable llamada "Path". Al hacerlo, presionamos en "Nuevo" y luego agregamos la dirección de instalación de python, en nuestro caso: "C:\Python27". Presionamos aceptar en todas las ventanas y la variable debería quedar agregada correctamente.

Una vez instalado, se debe instalar pip para agregar librerías a su sistema.

- Instalar pip: pip es el software usado para instalar librerías de Python, para su instalación debemos descargarlo desde https://bootstrap.pypa.io/pip/2.7/get-pip.py, en caso, que al entrar al link, no se los descargue automáticamente, basta con presionar las 2 teclas "CTRL + S", de esta forma les debería aparecer una ventana para poder guardar el archivo.

Para su instalación debemos abrir la ventana de Powershell. Para esto entramos a la carpeta donde se descargó el archivo y al mismo tiempo que se presiona la tecla "Shift" (la flecha hacia arriba que está sobre la tecla ctrl en la parte inferior izquierda de su teclado), se debe presionar click derecho de su ratón sobre cualquier parte en blanco de la carpeta. Entre las opciones debería ver "abrir la ventana de powershell aquí", o "abrir simbolo de sistema aquí".

Una vez con la ventana abierta debemos instalar el archivo descargado, para esto, escribimos en la consola "python get-pip.py" (sin comillas).

- Instalar pygame: Pygame es una librería de python, usaremos pip para poder instalarlo correctamente, para esto abrimos un simbolo de sistema (podemos abrirlo presionando la tecla Windows + R y luego escribir "cmd" en la ventana que aparecerá), y escribimos python -m pip install pygame

## Funcionamiento del sistema

Si se siguió correctamente la instalación de los paquetes, el uso del sistema es simple. Solo debemos abrir el Powershell en la carpeta del programa y escribir el comando "python .\EEG_new_version.py". El sistema le pedirá un nombre de archivo y luego usted debe presionar enter para iniciar el experimento.

Al terminar el experimento podrá ver una carpeta llamada "data", dentro de ella encontrará el experimento realizado con sus respuestas respectivas.
