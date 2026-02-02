# Cliente por consola de comandos para la API del T8 - Versión 0.1.0

El paquete Python desarrollado permite la comunicación con la API del T8 por consola de comandos, de una manera sencilla e intuitiva.




## Instalación y configuración

Para empezar, será necesario el paquete uv para realizar la construcción del paquete:

<pre>

$ pip install uv

</pre>

Tras instalar uv, se debe introducir el siguiente comando en la terminal:

<pre>

$ uv build

</pre>

Esto creará una carpeta `dist`, que contiene el archivo `.whl`, para realizar la instalación del paquete. Por lo que habrá que realizar el siguiente comando:

<pre>

$ uv pip install dist/t8apicliente-0.1.0-py3-none-any.whl

</pre>




Tras esto, el paquete ya está instalado, pero antes de empezar a usarlo, se deben definir las variables necesarias para la autenticación. Las variables imprescindibles son `T8_USER` y `T8_PASSWORD`.




Para ello, se pueden exportar al entorno:

<pre>

$ export T8_USER=< tu usuario >

$ export T8_PASSWORD=< tu contraseña >

</pre>




Por otro lado, también se pueden escribir en un archivo .env:

<pre>

# En el archivo .env

export T8_USER=< tu usuario >

export T8_PASSWORD=< tu contraseña >

</pre>

Y luego en la terminal:

<pre>

$ source .env

</pre>

Hay una tercera variable, el host (URL al endpoint `rest` del T8); esta se puede definir como se ha indicado para las otras dos, pero también se puede definir en el propio comando de la terminal, como se mostrará en el apartado de uso del paquete.




Una vez definidas las variables, ya está todo listo para empezar a usar el paquete. Ten en cuenta que estas variables se guardan en el contexto de la terminal, por lo que necesitarás volver a definirlas siempre que abras una nueva terminal.

## Uso del paquete

El paquete se utilizará mediante la terminal; el comando es `t8-cli`. Puedes hacer `t8-cli --help` para obtener una pequeña ayuda de los comandos disponibles.

### Opciones del CLI




Todos los comandos del paquete tienen sus opciones; sin embargo, antes de poner un comando, puedes escribir estas opciones relativas a la elección del host:

- `--host <ID>` o `-H <ID>`: Esta opción permite cambiar el host (o introducirlo); a diferencia del caso de la exportación de la variable, solo hace falta poner el identificador del host, es decir, no hace falta poner toda la URL.

- `--mirror` o `-R`: Esta opción solo hace algo si se utiliza a la vez que la anterior. Permite conectarse al backup del host en vez de al host real.




Es decir, para decidir el host en el comando, suponiendo que nos conectamos a un backup, se debe hacer lo siguiente:

<pre>

$ t8cli --host < ID del host > --mirror COMANDO [OPCIONES]

</pre>

Y en el caso de conectarse al host real:

<pre>

$ t8cli --host < ID del host > COMANDO [OPCIONES]

</pre>

Cabe resaltar que estas opciones no guardan el host en el contexto, por lo que será necesario poner el host en cada comando.

> Decisión de implementación: Si bien se podrían pasar las credenciales por consola de comandos, no parece lo más sensato a nivel de seguridad.




### Comandos List

Se han implementado dos comandos que listan instancias:




#### list-waves

Lista la fecha en formato ISO (timezone UTC) junto a su timestamp de todas las formas de onda disponibles para esa máquina, en ese punto y con ese modo de procesamiento.




La ayuda de la función devuelve lo siguiente:

<pre>

$ t8-cli list-waves --help

Usage: t8-cli list-waves [OPTIONS]




  Get list of waveform timestamps




Options:

  -P, --path TEXT       Path written as machine:point:proc_mode

  -M, --machine TEXT    Machine name

  -p, --point TEXT      Data point

  -m, --proc-mode TEXT  Processing mode

</pre>




#### list-spectra

Lista la fecha en formato ISO (timezone UTC) junto a su timestamp de todos los espectros disponibles para esa máquina, en ese punto y con ese modo de procesamiento.




La ayuda de la función devuelve lo siguiente:

<pre>

$ t8-cli list-spectra --help

Usage: t8-cli list-spectra [OPTIONS]




  Get list of spectra timestamps




Options:

  -P, --path TEXT       Path writen as machine:point:proc_mode

  -M, --machine TEXT    Machine name

  -p, --point TEXT      Data point

  -m, --proc-mode TEXT  Processing mode

</pre>




### Comandos get

Se han implementado dos comandos que obtienen datos de una instancia:




#### get-wave

Obtiene la forma de onda de un timestamp (o datetime) de un modo de procesamiento de un punto de una máquina. Si no se especifica el timestamp ni el datetime, se obtienen los datos más recientes. Esta forma de onda se guarda en el directorio `data\waves\` en formato JSON.




La ayuda de la función devuelve lo siguiente:

<pre>

$ t8-cli get-wave --help

Usage: t8-cli get-wave [OPTIONS]




  Get waveform data




Options:

  -P, --path TEXT       Path writen as machine:point:proc_mode

  -M, --machine TEXT    Machine name

  -p, --point TEXT      Data point

  -m, --proc-mode TEXT  Processing mode

  -t, --timestamp TEXT  Timestamp (default: latest)

  -d, --datetime TEXT   Datetime (optional)

</pre>




#### get-spectrum

Obtiene el espectro computado por el T8 de un timestamp (o datetime) de un modo de procesamiento de un punto de una máquina. Si no se especifica el timestamp ni el datetime, se obtienen los datos más recientes. Este espectro se guarda en el directorio `data\spectra\` en formato JSON.




La ayuda de la función devuelve lo siguiente:

<pre>

$ t8-cli get-spectrum --help

Usage: t8-cli get-spectrum [OPTIONS]




  Get spectra data




Options:

  -P, --path TEXT       Path writen as machine:point:proc_mode

  -M, --machine TEXT    Machine name

  -p, --point TEXT      Data point

  -m, --proc-mode TEXT  Processing mode

  -t, --timestamp TEXT  Timestamp (default: latest)

  -d, --datetime TEXT   Datetime (optional)

  </pre>

### Comandos plot

Se han implementado dos comandos que realizan gráficos de una instancia:




#### plot-wave

Obtiene el gráfico de la forma de onda de un timestamp (o datetime) de un modo de procesamiento de un punto de una máquina. Si no se especifica el timestamp ni el datetime, se obtienen los datos más recientes. Este plot se guarda en el directorio `data\plots\waves\` en formato png.




La ayuda de la función devuelve lo siguiente:

<pre>

$ t8-cli plot-wave --help

Usage: t8-cli plot-wave [OPTIONS]




  Plot waveform data




Options:

  -P, --path TEXT       Path writen as machine:point:proc_mode

  -M, --machine TEXT    Machine name

  -p, --point TEXT      Data point

  -m, --proc-mode TEXT  Processing mode

  -t, --timestamp TEXT  Timestamp (default: latest)

  -d, --datetime TEXT   Datetime (optional)

  </pre>




#### plot-spectrum

Obtiene el gráfico del espectro computado por el T8 de un timestamp (o datetime) de un modo de procesamiento de un punto de una máquina. Si no se especifica el timestamp ni el datetime, se obtienen los datos más recientes. Este plot se guarda en el directorio `data\plots\spectra\` en formato png.




La ayuda de la función devuelve lo siguiente:

<pre>

$ t8-cli plot-spectrum --help

Usage: t8-cli plot-spectrum [OPTIONS]




  Plot spectra data




Options:

  -P, --path TEXT       Path writen as machine:point:proc_mode

  -M, --machine TEXT    Machine name

  -p, --point TEXT      Data point

  -m, --proc-mode TEXT  Processing mode

  -t, --timestamp TEXT  Timestamp (default: latest)

  -d, --datetime TEXT   Datetime (optional)

  </pre>

### Otros comandos

Se ha desarrollado un comando que no entra dentro de los grupos anteriores.

#### compute-spectrum

Computa un espectro utilizando la FFT de la librería `numpy` a partir de una forma de onda.




La ayuda de la función devuelve lo siguiente:

<pre>

$ t8-cli compute-spectrum --help

Usage: t8-cli compute-spectrum [OPTIONS]




  Compute and plot spectrum from waveform file




Options:

  -w, --wave TEXT  Waveform file path  [required]

</pre>




## Tests

Se ha realizado un directorio `tests` con tests unitarios para comprobar el correcto funcionamiento del código desarrollado. Para simular las llamadas a la API se han utilizado mocks; de esta forma no se depende de la disponibilidad del T8 para comprobar el funcionamiento del paquete.




Para ejecutar los tests:

<pre>

$ uv run pytest

</pre>




## Scripts

Se ha realizado un directorio `scripts` con scripts de utilidad.




En este directorio se encuentran:

- `compare_spectra.py`: Una vez en el directorio `data\spectra`, se dispone del json tanto del T8 como computado; para un mismo path, ejecutar este código pasando como argumento el path relativo al json del T8 hará que se guarde una imagen en `data\plots\` llamada `comparision_spectrum.png`. En esta imagen están graficados tanto el espectro computado como el del T8, uno al lado del otro.




- `b64decode.ipynb`: Notebook que se utilizó para averiguar el método de compresión que utiliza el T8 y el tipo de datos que envía. Actualmente, no es ejecutable, ya que el método `decode()` de las dataclass no devuelve el array de bytes resultado de descodificar los datos en base 64. Este notebook está en el repositorio para la comprensión de la estructura (tipo de datos, compresión y cifrado) utilizada por el T8.