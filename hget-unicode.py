#!/usr/bin/env python
# encoding: utf-8
"""
hget: un cliente HTTP simple

Escrito con fines didacticos por la catedra de
Redes y Sistemas Distribuidos,
FaMAF-UNC

El proposito de este codigo es mostrar con un ejemplo concreto las primitivas
basicas de comunicacion por sockets; no es para uso en produccion (para eso
esta el modulo urllib de la biblioteca estandar de python que contiene un
cliente HTTP mucho mas completo y correcto.
Revision 2019 (a Python 3): Pablo Ventura
Revision 2011: Eduardo Sanchez
Original 2009-2010: Natalia Bidart, Daniel Moisset

"""

import sys
import socket
import optparse
import idna

PREFIX = "http://"
HTTP_PORT = 80   # El puerto por convencion para HTTP,
# según http://tools.ietf.org/html/rfc1700
HTTP_OK = "200"  # El codigo esperado para respuesta exitosa.
HTTP_REDIRECTS = ["301", "302"]


def parse_server(url):
    """
    Obtiene el server de una URL. Por ejemplo, si recibe como input
    "http://www.famaf.unc.edu.ar/carreras/computacion/computacion.html"
    devuelve "www.famaf.unc.edu.ar"

    El llamador es el dueño de la memoria devuelta

    Precondicion: url es un str, comienza con PREFIX
    Postcondicion:
        resultado != NULL
        url comienza con PREFIX + resultado
        '/' not in resultado
        resultado es la cadena mas larga posible que cumple lo anterior

    >>> parse_server('http://docs.python.org/library/intro.html')
    'docs.python.org'

    >>> parse_server('http://google.com')
    'google.com'

    >>> parse_server('google.com') # Falta el prefijo, deberia fallar
    Traceback (most recent call last):
       ...
    AssertionError

    """
    assert url.startswith(PREFIX)
    # Removemos el prefijo:
    path = url[len(PREFIX):]
    path_elements = path.split('/')
    result = path_elements[0]

    assert result != None
    assert url.startswith(PREFIX + result)
    assert '/' not in result
    return result


def connect_to_server(server_name):
    """
    Se conecta al servidor llamado server_name

    Devuelve el socket conectado en caso de exito, o falla con una excepcion
    de socket.connect / socket.gethostbyname.

    >>> type(connect_to_server('www.famaf.unc.edu.ar')) # doctest: +ELLIPSIS
    <class 'socket.socket'>

    >>> connect_to_server('no.exis.te') # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    gaierror: [Errno -5] No address associated with hostname

    >>> connect_to_server('localhost')
    Traceback (most recent call last):
       ...
    ConnectionRefusedError: [Errno 111] Connection refused
    """

    # Buscar direccion ip
    # COMPLETAR ABAJO DE ESTA LINEA
    ip_address = socket.gethostbyname(server_name)
    # Aqui deberian obtener la direccion ip del servidor y asignarla
    # a ip_address
    # DEJAR LA LINEA SIGUIENTE TAL COMO ESTA
    sys.stderr.write("Contactando al servidor en %s...\n" % ip_address)
    # Crear socket
    # COMPLETAR ABAJO DE ESTA LINEA
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Aqui deben conectarse al puerto correcto del servidor
    s.connect((server_name, HTTP_PORT))
    return s
    # NO MODIFICAR POR FUERA DE ESTA FUNCION


def send_request(connection, url):
    """
    Envia por 'connection' un pedido HTTP de la URL dada

    Precondicion:
        connection es valido y esta conectado
        url.startswith(PREFIX)
    """
    HTTP_REQUEST = b"GET %s HTTP/1.0\r\n\r\n"

    connection.send(HTTP_REQUEST % url.encode())


def read_line(connection):
    """
    Devuelve una linea leida desde 'connection`; hasta el siguiente '\n'
    (incluido), o hasta que se terminen los datos.

    Si se produce un error, genera una excepcion.
    """
    result = b''
    error = False
    # Leer de a un byte
    try:
        data = connection.recv(1)
    except:
        error = True
    while not error and data != b'' and data != b'\n':
        result = result + data
        try:
            data = connection.recv(1)
        except:
            error = True
    if error:
        raise Exception("Error leyendo de la conexion!")
    else:
        result += data  # Add last character
        return result


def check_http_response(header):
    """
    Verifica que el encabezado de la respuesta este bien formado e indique
    éxito. Un encabezado de respuesta HTTP tiene la forma

    HTTP/<version> <codigo> <mensaje>

    Donde version tipicamente es 1.0 o 1.1, el codigo para exito es 200,
    y el mensaje es opcional y libre pero suele ser una descripcion del
    codigo.

    >>> check_http_response(b"HTTP/1.1 200 Ok")
    True

    >>> check_http_response(b"HTTP/1.1 200")
    True

    >>> check_http_response(b"HTTP/1.1 301 Permanent Redirect")
    False

    >>> check_http_response(b"Malformed")
    False
    """
    header = header.decode()
    elements = header.split(' ', 3)
    return (len(elements) >= 2 and elements[0].startswith("HTTP/")
            and elements[1] == HTTP_OK)


def get_response(connection, filename):
    """
    Recibe de `connection` una respuesta HTTP, y si es válida la descarga
    en un archivo llamado `filename`.

    Devuelve True en caso de éxito, False en caso contrario.
    Si la respuesta es una redirección 301 o 302, devuelve la nueva URL.
    """
    BUFFER_SIZE = 4096

    # Verificar estado
    header = read_line(connection)
    if not check_http_response(header):
        header_str = header.decode().strip()
        sys.stdout.write(f"Encabezado HTTP malformado: '{header_str}'\n")

        # Manejo de redirección
        if header_str.startswith("HTTP/1.1 301") or header_str.startswith("HTTP/1.1 302"):
            sys.stdout.write("Redirección detectada...\n")

            # Leer los encabezados para encontrar Location
            new_url = None
            while True:
                line = read_line(connection).decode().strip()
                if line.lower().startswith("location:"):
                    new_url = line.partition(":")[2].strip()
                    break
                if line == "":  # Fin de los headers
                    break

            if new_url:
                sys.stdout.write(f"Redirigiendo a: {new_url}\n")
                # Verificar si la URL redirigida es HTTPS
                if new_url.startswith("https://"):
                    sys.stdout.write("Redirección a HTTPS detectada. El programa terminará aquí.\n")
                    return False  # Terminar el proceso sin error

                else:
                    return new_url  # Continuar con HTTP si no es HTTPS

        return False
    else:
        # Saltar el resto del encabezado
        while read_line(connection) not in [b'\r\n', b'']:
            pass

        # Descargar los datos al archivo
        with open(filename, "wb") as output:
            data = connection.recv(BUFFER_SIZE)
            while data:
                output.write(data)
                data = connection.recv(BUFFER_SIZE)

        return True


def download(url, filename):
    server = parse_server(url)
    sys.stderr.write(f"Contactando servidor '{server}'...\n")
    
    try:
        connection = connect_to_server(server)
    except socket.gaierror:
        sys.stderr.write(f"No se encontró la dirección '{server}'\n")
        sys.exit(1)
    except socket.error:
        sys.stderr.write(f"No se pudo conectar al servidor HTTP en '{server}:{HTTP_PORT}'\n")
        sys.exit(1)

    try:
        sys.stderr.write("Enviando pedido...\n")
        send_request(connection, url)
        sys.stderr.write("Esperando respuesta...\n")
        result = get_response(connection, filename)
        
        if isinstance(result, str):  # Si es una URL, manejar la redirección
            sys.stderr.write(f"Redirigiendo a: {result}\n")
            connection.close()
            return download(result, filename)  # Llamada recursiva

        if not result:
            sys.stderr.write("No se pudieron descargar los datos\n")
    except Exception as e:
        sys.stderr.write(f"Error al comunicarse con el servidor: {e}\n")
        sys.exit(1)


#Funciones Extra para Punto estrella
def nonASCIIchar(url:str):
    """Verifica si la URL tiene caracteres Unicode (fuera del rango ASCII)."""
    affirmative = any(ord(c) > 127 for c in url)
    if affirmative:
        print("URL con caracteres Unicode detectados...")
    return affirmative

# def convertASCIIchar(unicode_domain:str):
#     """Convierte un dominio Unicode a su equivalente Punycode."""   
#     assert unicode_domain.startswith(PREFIX)
#     unicode_domain = unicode_domain[7:]
#     domain_parts = unicode_domain.split('/')[0]
#     punycode_domain = PREFIX+idna.encode(domain_parts).decode()+"/"
#     print(f"Dominio convertido a -> {punycode_domain}")
#     return punycode_domain

def convertASCIIchar(unicode_url: str):
    """Convierte una URL con dominio Unicode a su equivalente Punycode."""
    assert unicode_url.startswith(PREFIX)
    url_without_prefix = unicode_url[len(PREFIX):]  # Quita "http://"
    domain = url_without_prefix.split('/')[0]  # Extrae el dominio
    path = url_without_prefix[len(domain):]  # Extrae la ruta (si existe)

    punycode_domain = idna.encode(domain).decode()  # Convierte dominio a Punycode
    converted_url = PREFIX + punycode_domain + path  # Reconstruye la URL completa

    print(f"Dominio convertido a -> {converted_url}")
    return converted_url



def main():
    """Procesa los argumentos, y llama a download()"""
    # Parseo de argumentos
    parser = optparse.OptionParser(usage="usage: %prog [options] http://...")
    parser.add_option("-o", "--output", help="Archivo de salida",
                      default="download.html")
    options, args = parser.parse_args()
    if len(args) != 1:
        sys.stderr.write("No se indico una URL a descargar\n")
        parser.print_help()
        sys.exit(1)

    # Validar el argumento
    url = args[0]
    if not url.startswith(PREFIX):
        sys.stderr.write("La direccion '%s' no comienza con '%s'\n" % (url,
                                                                       PREFIX))
        sys.exit(1)


    if nonASCIIchar(url):
        url = convertASCIIchar(url) 

    download(url, options.output)


if __name__ == "__main__":
    main()
    sys.exit(0)
