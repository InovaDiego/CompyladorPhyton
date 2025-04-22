import tkinter as tk
from tkinter import ttk
from analizador_lexico import AnalizadorLexico, TOKENS

class main():
   

    codigo_fuente = input("Ingresa el código fuente: ")

    #  Crear una instancia del analizador léxico
    analizador = AnalizadorLexico(TOKENS)

    tokens = analizador.analizar(codigo_fuente)

  
    ventana = tk.Tk()
    ventana.title("Analizador Léxico")


    tabla = ttk.Treeview(ventana, columns=("Token", "Tipo"), show="headings")
    tabla.heading("Token", text="Token")
    tabla.heading("Tipo", text="Tipo")
    tabla.pack(padx=10, pady=10)

    for token, tipo in tokens:
        tabla.insert("", tk.END, values=(token, tipo))


    ventana.mainloop()

if __name__ == "__main__":
    main()