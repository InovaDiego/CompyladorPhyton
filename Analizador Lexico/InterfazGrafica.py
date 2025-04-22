import tkinter as tk
class InterfazGrafica:
    def __init__(self, root, analizador):
        self.root = root
        self.root.title("Analizador Léxico")
        self.analizador = analizador

        self.codigo_fuente_label = tk.Label(root, text="Código Fuente:")
        self.codigo_fuente_label.pack()

        self.codigo_fuente_text = tk.Text(root, height=10, width=50)
        self.codigo_fuente_text.pack()

        self.analizar_button = tk.Button(root, text="Analizar", command=self.analizar_codigo)
        self.analizar_button.pack()

        self.tokens_label = tk.Label(root, text="Tokens:")
        self.tokens_label.pack()

        self.tokens_text = tk.Text(root, height=10, width=50)
        self.tokens_text.pack()

        self.errores_label = tk.Label(root, text="Errores:")
        self.errores_label.pack()

        self.errores_text = tk.Text(root, height=10, width=50)
        self.errores_text.pack()

    def analizar_codigo(self):
        codigo_fuente = self.codigo_fuente_text.get("1.0", tk.END)
        tokens, errores = self.analizador.analizar(codigo_fuente)

        self.tokens_text.delete("1.0", tk.END)
        self.errores_text.delete("1.0", tk.END)

        if tokens:
            for token, tipo in tokens:
                self.tokens_text.insert(tk.END, f"[{token}, {tipo}]\n")
        if errores:
            for error in errores:
                self.errores_text.insert(tk.END, f"{error}\n")