# Convertidor de enteros con signo y codificación de texto

Aplicación web desarrollada con **Python 3.12 y Django** para representar enteros con signo mediante complemento a dos y analizar la codificación de caracteres Unicode. Utiliza SQLite para almacenar el historial de conversiones numéricas y Docker para ejecutar la aplicación en un entorno aislado.

## Funcionalidades

- Conversión de enteros decimales positivos y negativos con representación de 8, 16 y 32 bits.
- Validación de rangos según el complemento a dos.
- Representación binaria con el ancho seleccionado y agrupación de cuatro bits, hexadecimal y octal.
- Identificación del bit de signo e interpretación del patrón como entero sin signo.
- Análisis de textos de hasta 15 caracteres, mostrando el punto de código Unicode, los bytes UTF-8 y las longitudes en UTF-8 y UTF-16.
- Almacenamiento y consulta de las últimas 10 conversiones numéricas mediante SQLite.
- Validación de entradas y mensajes de error para datos vacíos, valores no numéricos, números fuera de rango y textos demasiado largos.
- Pruebas automatizadas para conversiones numéricas, validaciones y codificación de caracteres.

## Requisitos

- Docker y Docker Compose.

## Ejecución con Docker

Construir la imagen e iniciar la aplicación:

```bash
docker compose up --build -d
```

Aplicar las migraciones de Django:

```bash
docker compose run --rm web python manage.py migrate
```

Acceder a la aplicación desde el navegador:

http://localhost:8000

Consultar los registros de ejecución:

```bash
docker compose logs -f web
```

Consultar el consumo de recursos del contenedor:

```bash
docker stats --no-stream
```

Detener los servicios:

```bash
docker compose down
```

La configuración de Compose establece un límite de **512 MB de memoria RAM y 0.5 CPU** para el contenedor de la aplicación.

## Persistencia del historial

La base de datos SQLite se almacena en el directorio `data/`, montado como volumen desde el equipo anfitrión hacia el contenedor. Esto permite conservar los registros al eliminar y recrear el contenedor, siempre que se mantenga el directorio persistente.

Para recrear el contenedor:

```bash
docker compose down
docker compose up --build -d
```

El historial previamente almacenado permanece disponible porque los datos se conservan fuera del ciclo de vida del contenedor.

## Representación de números negativos y ALU

La unidad aritmético-lógica (ALU) realiza operaciones aritméticas y lógicas sobre valores binarios. En los sistemas digitales, el complemento a dos permite representar números negativos utilizando una cantidad fija de bits.

Para obtener la representación de un número negativo, se invierten los bits de su valor positivo y se suma uno. Por ejemplo, en 8 bits, el número \(-5\) se representa como `11111011`.

La suma se realiza mediante circuitos sumadores binarios, tanto para operandos positivos como negativos. El patrón resultante se interpreta según el ancho de bits y la representación utilizada. En complemento a dos, el bit más significativo indica el signo: `0` representa un valor no negativo y `1` uno negativo. Si el resultado excede el rango representable, puede producirse un desbordamiento aritmético.

## Contenedores y máquinas virtuales

Un contenedor ejecuta una aplicación en un entorno aislado y comparte el kernel del sistema operativo anfitrión. Una máquina virtual utiliza un hipervisor para ejecutar un sistema operativo invitado completo.

Los contenedores generalmente requieren menos recursos y tienen tiempos de inicio menores. Las máquinas virtuales, por su parte, permiten ejecutar sistemas operativos diferentes y proporcionan aislamiento a nivel de sistema operativo.

## Pruebas automatizadas

Ejecutar las pruebas de la aplicación:

```bash
docker compose run --rm web python manage.py test conversor_repo -v 2
```

Las pruebas cubren conversiones de números negativos en 8 bits, un valor positivo en 16 bits, validaciones de rango y análisis de texto con caracteres Unicode, incluyendo `ñ` y emojis.
