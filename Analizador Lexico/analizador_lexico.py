import re
import tkinter as tk
import sys


TOKENS = {
    "PALABRA_Reservada": sorted([
        "False", "None", "True", "as", "assert", "async", "await",
        "class", "continue", "def", "del", "except", "finally",
        "from", "global", "import", "in", "is", "lambda", "nonlocal",
        "pass", "raise", "with", "yield", "print", "println", "int"
    ], key=len, reverse=True),
    "Bucle": ["if", "else", "while", "try", "return", "elif", "break", "for"],
    "IDENTIFICADOR": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "NUMERO_FLOTANTE": r"\d*\.\d+",
    "NUMERO_ENTERO": r"\d+",
    "CADENA": r'"[^"]*"',
    "OPERADOR": ["==", "!=", "<=", ">=", "=", "+=", "-=", "*=", "/=", "+", "-", "*", "/", "<", ">"],
    "OPERADOR_LOGICO": ["and", "or", "not"],
    "SIGNO": [ ":", ".", ";", "@", "%", "#", "!", "°", "|", "?", "'", "¡", "¿", "$", "'", "&", "^"],
    "PARENTESIS": ["(", ")"],
    "LLAVE": ["{", "}"],
    "CORCHETE": ["[", "]"],
    "COMENTARIO_LINEA": r"//.*",
    "ESPACIO_BLANCO": r"\s+"
}

class AnalizadorLexico:
    def __init__(self, tokens):
        self.TOKENS = tokens

    def analizar(self, codigo_fuente):
        tokens = []
        errores = []
        posicion = 0
        while posicion < len(codigo_fuente):
            match = None
            for tipo_token, patron in self.TOKENS.items():
                if isinstance(patron, list):
                    for valor in patron:
                        if codigo_fuente[posicion:].startswith(valor):
                            match = (valor, tipo_token)
                            break
                    if match:
                        break
                else:
                    regex = re.compile(patron)
                    resultado = regex.match(codigo_fuente, posicion)
                    if resultado:
                        match = (resultado.group(0), tipo_token)
                        break
            if match:
                if match[1] != "ESPACIO_BLANCO":
                    tokens.append(match)
                    posicion += len(match[0])
                else:
                    posicion += len(match[0])
            else:
                errores.append(f"Carácter no válido: {codigo_fuente[posicion]}")
                posicion += 1
        return tokens, errores