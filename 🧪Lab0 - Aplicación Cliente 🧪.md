# Conceptos adquiridos
> [!TIP] 
> ### Para obtener la **IP** de un servidor por **server_name**:
```python
import socket
servername = "http://www.google.com/"
ip_address = socket.getbyhostname(servername)
```

 >[!TIP] 
 >### Para crear un **socket** y conectarlo a la **IP**
```python
s = socket.socket((socket.AF_INET, socket.SOCK_STREAM))
#AF_INET perteneciente al protocolo IPV4
#SOCK_STREAM -> TCP para HTTP
 ```

> [!NOTE]
> ###  Si deseáramos tener en nuestra **URL** algo como:
> http://中文.tw/
> https://.la💩2
> Los dominios como estos funcionan gracias a un sistema llamado **IDN (Internationalized Domain Names)**, que permite el uso de caracteres **Unicode** en nombres de dominios.
> Lo que debemos tener en cuenta que **la infraestructura de internet** sólo entiende caracteres **ASCII**, por lo que los dominios que no tienen este tipo de caracteres deben codificarse de una manera especial para que los servidores los reconozcan.
> El mecanismo de codificación principal es **Punycode**, que convierte caracteres de Unicode en ASCII compatible con el DNS (Domain Name System)

