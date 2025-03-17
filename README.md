# 🧪 Laboratorio 0 - Aplicación Cliente 👤

# 🤓 Punto Estrella ✨

Cuáles son los mecanismos que permiten funcionar a nombres de dominios como:

> - http://中文.tw/
> - https://💩.la

🤔

Primero y principal debemos saber que los caracteres chinos y emojis no son válidos para ser utilizados en un nombre de dominio, porque los nombres de dominio solo pueden contener caracteres ASCII (análogamente se aplica para todo tipo de caracter que se utilice que sea no ASCII). Por lo tanto, para que estos nombres de dominio funcionen, se debe realizar un proceso de conversión de los caracteres no válidos a caracteres válidos, o también llamado `encoding`.

Este tipo de caracteres forman parte de un conjunto llamado `Unicode`, que es un estándar que permite a los usuarios representar y manipular texto de cualquier idioma en sus computadoras. Para poder representar estos caracteres en un nombre de dominio válido se utiliza un sistema de codificación llamado `Punycode`.

![img](./imgs/1.png)

_Logo de Unicode_

> [!NOTE]
>
> ## Punycode
>
> A dicho sistema de codificación lo proporciona la librería de Python `idna`, la cual
> se encarga de convertir nombres de dominio Unicode a nombres de dominio ASCII compatibles con el sistema de nombres de dominio (DNS).

## 🐍 Código

Se agregaron algunas línes de código al archivo `hget.py` y se creó un nuevo archivo llamado `hget-unicode.py` para poder realizar la conversión de nombres de dominio Unicode a ASCII y a su vez tener en cuenta las redirecciones de las páginas web.

Se tuvieron en cuenta las siguientes consideraciones:

- Se utilizó la librería `idna` para realizar la conversión de nombres de dominio Unicode a ASCII.
- Se utilizó la función `idna.encode()` para realizar la conversión.
- Se definió una función llamada `nonASCIIchar()`, la cual verifica si la URL tiene caracteres Unicode (fuera del rango ASCII).
- Se definió una función llamada `convertASCIIchar()`, la cual convierte una URL con dominio Unicode a su equivalente Punycode.
- En la función `main()`, se verifica si la URL tiene caracteres Unicode y si es así, se convierte a su equivalente Punycode.

  ```python
      if nonASCIIchar(url):
          url = convertASCIIchar(url)

      #Entrada http://ñandú.cl
      #Conversión -> http://xn--and-6ma2c.cl
  ```

- Manejo de las redirecciones HTTP (códigos 301 y 302): Si la redirección es a https://, se interrumpe el proceso con un mensaje. Si la redirección es a http://, se realiza la petición a la nueva URL.
- En la estructura de `download()`, se agregó código para manejar errores sin terminar el programa abruptamente.

  ```python
      while True:
          if status_code == 301 or status_code == 302:
              url = headers['Location']
              status_code, headers, body = get(url)
          else:
              break
  ```

# 🫡 Conclusiones

Este código a simple ejecución tiene la misma funcionalidad que `hget.py` teniendo en cuenta las consideraciones mencionadas anteriormente. Se puede observar que la conversión de nombres de dominio Unicode a ASCII es un proceso sencillo y rápido de realizar, gracias a la librería `idna` que nos proporciona Python.

Por otro lado, si se prueba en ambos programas con la misma entrada se puede obtener el mismo resultado, es decir, con ambos códigos se obtiene **éxito** al realizar la petición a dicha página web. En principio me resultó un poco confuso ver que en ambos códigos funcionaba de la misma manera, pero luego de investigar un poco más, pude entender que la librería `socket` de Python ya realiza la conversión de nombres de dominio Unicode a ASCII de manera automática, por lo que no era necesario realizar la conversión manualmente.

Además desde hace tiempo, la mayoría de los navegadores web soportan nombres de dominio Unicode, por lo que no es necesario realizar la conversión manualmente, ya que los navegadores se encargan de realizar la conversión de manera automática (Incluyendo que la librería de sockets ya lo hace).

Me sirvió mucho este laboratorio para entender cómo funcionan los nombres de dominio Unicode y cómo se realiza la conversión de estos a ASCII, además de aprender cómo se realiza una petición HTTP a una página web utilizando Python y librerías como `socket` e `idna`.

# Dependencias

1. Crear y activar entorno virtual

```bash
python3 -m venv venv
```

2. Instalar dependencias. La única librería que se utilizó fuera del standard library de python es `idna`, para instalarla se puede hacer de la siguiente manera:

```bash
pip install idna
```

3. Salir del entorno virtual

```bash
deactivate
```

# Ejecución

```bash
python hget-unicode.py http://ñandú.cl
```

Opcional para indicar el renombramiento del archivo de salida:

```bash
python hget-unicode.py http://ñandú.cl -o 4example.html
```
