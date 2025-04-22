import sys
from InterfazGrafica import InterfazGrafica
from analizador_lexico import TOKENS, AnalizadorLexico
import tkinter as tk

class InterfazLineaComandos:
    def __init__(self, analizador):
        self.analizador = analizador

    def ejecutar(self):
        while True:
            try:
                codigo_fuente = input("Ingrese el código fuente (o 'salir' para terminar): ")
            except EOFError:
                break  # Salir del bucle si se encuentra EOF

            if codigo_fuente.lower() == "salir":
                break

            tokens, errores = self.analizador.analizar(codigo_fuente)

            if tokens:
                print("Tokens:")
                for token, tipo in tokens:
                    print(f"[{token}, {tipo}]")
            if errores:
                print("Errores:")
                for error in errores:
                    print(error)

if __name__ == "__main__":
    analizador = AnalizadorLexico(TOKENS)

    # El usuario elige la interfaz
    modo = "c"  # Modo predeterminado para entornos no interactivos
    if sys.stdin.isatty():
        try:
            modo = input("¿Interfaz gráfica (g) o línea de comandos (c)? ")
        except EOFError:
            pass  # No hacer nada si hay EOF en la entrada interactiva

    if modo.lower() == "g":
        root = tk.Tk()
        app = InterfazGrafica(root, analizador)
        root.mainloop()
    elif modo.lower() == "c":
        app = InterfazLineaComandos(analizador)
        app.ejecutar()
    else:
        print("Modo no válido.")