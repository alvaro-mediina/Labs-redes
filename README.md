# 🧪 Laboratorio 0 - Aplicación Cliente 👤

# 🙂‍↕️ Punto Estrella ✨

> [!Note] ### Mecanismos que permiten funcionar a nombres de dominios como:
>
> - http://中文.tw/
> - https://💩.la

Primero y principal debemos saber que los caracteres chinos y emojis no son válidos para ser utilizados en un nombre de dominio, porque los nombres de dominio solo pueden contener caracteres ASCII. Por lo tanto, para que estos nombres de dominio funcionen, se debe realizar un proceso de conversión de los caracteres no válidos a caracteres válidos, o también llamado `encoding`.

Este tipo de caracteres forman parte de un conjunto de caracteres llamado `Unicode`, que es un estándar que permite a los usuarios representar y manipular texto de cualquier idioma en sus computadoras. Para poder representar estos caracteres en un nombre de dominio válido se utiliza un sistema de codificación llamado `Punycode`.

![img](/imgs/1.png)

_Logo de Unicode_

> [!Note] ### Punycode
> A dicho sistema de codificación lo proporciona la librería de Python `idna`, la cual
> se encarga de convertir nombres de dominio Unicode a nombres de dominio ASCII compatibles con el sistema de nombres de dominio (DNS).

## Ejemplos de uso

- http://www.ñandú.cl

# Dependencias

1. Crear y activar entorno virtual

```bash
python3 -m venv venv
```

2. Instalar dependencias
   La única librería que se utilizó fuera del standard library de python es `idna`, para instalarla se puede hacer de la siguiente manera:

```bash
pip install idna
```

3. Salir del entorno virtual

```bash
deactivate
```
