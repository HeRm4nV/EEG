# Tutorial para uso de EEG

## Instalación de paquetes y librerías

Antes del uso normal del sistema se requiere tener instalado en Windows "Python", para verificar la instalación puede presionar inicio en la parte inferior izquierda de su pantalla y escribir "Python" (no es necesario presionar algo más, solo de click en inicio y escriba sin seleccionar nada, el sistema operativo buscará automáticamente).

En caso que no esté instalado puede instalarlo desde:

https://www.python.org/downloads/release/python-2718/

Solo debe descargar el archivo "Windows x86-64 MSI installer" para los dispositivos con windows 64bits o en caso contrario "Windows x86 MSI installer" para los de 32bits y seguir los pasos de instalación, asegurandose que al final se agregue python al "PATH de Windows".

Una vez instalado, si se desea puede instalar pip para agregar librerías a su sistema instalar pip.

- Instalar pip: pip es el software usado para instalar librerías de Python, para su instalación debemos descargarlo desde https://bootstrap.pypa.io/get-pip.py, en caso, que al entrar al link, no se los descargue automáticamente, basta con presionar las 2 teclas "CTRL + S", de esta forma les debería aparecer una ventana para poder guardar el archivo.

Para su instalación debemos abrir la ventana de Powershell. Para esto entramos a la carpeta donde se descargó el archivo y al mismo tiempo que se presiona la tecla "Shift" (la flecha hacia arriba que está sobre la tecla ctrl en la parte inferior izquierda de su teclado), se debe presionar click derecho de su ratón sobre cualquier parte en blanco de la carpeta. Entre las opciones debería ver "abrir la ventana de powershell aquí", o "abrir simbolo de sistema aquí".

Una vez con la ventana abierta debemos instalar el archivo descargado, para esto, escribimos en la consola "python get-pip.py" (sin comillas).

## Funcionamiento del sistema

Si se siguió correctamente la instalación de los paquetes, el uso del sistema es simple. Solo debemos abrir el Powershell en la carpeta del programa y escribir el comando "python .\EEG_new_version.py". El sistema le pedirá un nombre de archivo y luego usted debe presionar enter para iniciar el experimento.

Al terminar el experimento podrá ver una carpeta llamada "data", dentro de ella encontrará el experimento realizado con sus respuestas respectivas.
