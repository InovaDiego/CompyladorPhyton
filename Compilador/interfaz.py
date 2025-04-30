import tkinter as tk
from tkinter import ttk, scrolledtext
from lexico import AnalizadorLexico
from sintactico import AnalizadorSintactico
from semantico import AnalizadorSemantico

class InterfazLexico:
    def __init__(self, root):
        self.root = root
        self.analizador_lexico = AnalizadorLexico()
        self.analizador_sintactico = AnalizadorSintactico()
        self.analizador_semantico = AnalizadorSemantico()
        
        # Configuración de la ventana principal
        self.root.title("COMPILADOR")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        # Frame principal
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  
        
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Área de código fuente
        tk.Label(self.frame, text="Codigo Python:", 
                font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky="w")
        
        self.entrada_codigo = scrolledtext.ScrolledText(
            self.frame,
            width=100,
            height=20,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg='#000000',
            fg='white',
            insertbackground='white'
        )
        self.entrada_codigo.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        # Frame para botones
        self.frame_botones = tk.Frame(self.frame)
        self.frame_botones.grid(row=2, column=0, pady=5)
        
        # Botón

        self.boton_analizar = tk.Button(
            self.frame_botones,
            text="Analizador Lexico",
            command=self.analizar_codigo,
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=15,
            pady=8
        )
        self.boton_analizar.pack(side=tk.LEFT, padx=5)
        
        # Botón de análisis sintáctico
        self.boton_sintactico = tk.Button(
            self.frame_botones,
            text="Analizador Sintactico",
            command=self.analizar_sintactico,
            font=('Arial', 11, 'bold'),
            bg='#2196F3',
            fg='white',
            padx=15,
            pady=8
        )
        self.boton_sintactico.pack(side=tk.LEFT, padx=5)
        
        # Botón de análisis semántico
        self.boton_semantico = tk.Button(
            self.frame_botones,
            text="Analizador Semantico",
            command=self.analizar_semantico,
            font=('Arial', 11, 'bold'),
            bg='#FF9800',
            fg='white',
            padx=15,
            pady=8
        )
        self.boton_semantico.pack(side=tk.LEFT, padx=5)
        
        # Panel de resultados
        self.panel_resultados = ttk.Notebook(self.frame)
        self.panel_resultados.grid(row=3, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(3, weight=1)
        
        # Pestañas
        self.configurar_pestana_tokens()
        self.configurar_pestana_errores()
        self.configurar_pestana_sintactico()
        self.configurar_pestana_semantico()
        
        # Barra de estado
        self.barra_estado = tk.Frame(self.frame)
        self.barra_estado.grid(row=4, column=0, sticky="ew", pady=(5, 0))

        self.label_tokens = tk.Label(
            self.barra_estado,
            text="Tokens: 0",
            font=('Arial', 10),
            padx=10
        )
        self.label_tokens.pack(side=tk.LEFT)
        
        self.label_errores = tk.Label(
            self.barra_estado,
            text="Errores: 0",
            font=('Arial', 10),
            fg="red",
            padx=10
        )
        self.label_errores.pack(side=tk.LEFT)
        
        self.label_sintactico = tk.Label(
            self.barra_estado,
            text="Sintáctico: 0",
            font=('Arial', 10),
            fg="blue",
            padx=10
        )
        self.label_sintactico.pack(side=tk.LEFT)
        
        self.label_semantico = tk.Label(
            self.barra_estado,
            text="Semántico: 0",
            font=('Arial', 10),
            fg="orange",
            padx=10
        )
        self.label_semantico.pack(side=tk.LEFT)
    
    def configurar_pestana_tokens(self):
        self.tab_tokens = tk.Frame(self.panel_resultados)
        self.panel_resultados.add(self.tab_tokens, text="Tokens")
        
        self.tree_tokens = ttk.Treeview(
            self.tab_tokens,
            columns=('Tipo', 'Valor', 'Línea', 'Columna', 'Posición'),
            show='headings',
            selectmode='browse'
        )
        
        columnas = [
            ('Tipo', 150, 'w'),
            ('Valor', 300, 'w'),
            ('Línea', 60, 'center'),
            ('Columna', 70, 'center'),
            ('Posición', 80, 'center')
        ]
        
        for col, width, anchor in columnas:
            self.tree_tokens.heading(col, text=col)
            self.tree_tokens.column(col, width=width, anchor=anchor)
        
        vsb = ttk.Scrollbar(self.tab_tokens, orient="vertical", command=self.tree_tokens.yview)
        hsb = ttk.Scrollbar(self.tab_tokens, orient="horizontal", command=self.tree_tokens.xview)
        self.tree_tokens.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree_tokens.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        self.tab_tokens.grid_rowconfigure(0, weight=1)
        self.tab_tokens.grid_columnconfigure(0, weight=1)
    
    def configurar_pestana_errores(self):
        self.tab_errores = tk.Frame(self.panel_resultados)
        self.panel_resultados.add(self.tab_errores, text="Lexico")
        
        self.tree_errores = ttk.Treeview(
            self.tab_errores,
            columns=('Tipo', 'Mensaje', 'Línea', 'Columna', 'Posición'),
            show='headings',
            selectmode='browse'
        )
        
        columnas = [
            ('Tipo', 120, 'w'),
            ('Mensaje', 350, 'w'),
            ('Línea', 60, 'center'),
            ('Columna', 70, 'center'),
            ('Posición', 80, 'center')
        ]
        
        for col, width, anchor in columnas:
            self.tree_errores.heading(col, text=col)
            self.tree_errores.column(col, width=width, anchor=anchor)
        
        vsb = ttk.Scrollbar(self.tab_errores, orient="vertical", command=self.tree_errores.yview)
        hsb = ttk.Scrollbar(self.tab_errores, orient="horizontal", command=self.tree_errores.xview)
        self.tree_errores.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree_errores.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        self.tab_errores.grid_rowconfigure(0, weight=1)
        self.tab_errores.grid_columnconfigure(0, weight=1)
    
    def configurar_pestana_sintactico(self):
        self.tab_sintactico = tk.Frame(self.panel_resultados)
        self.panel_resultados.add(self.tab_sintactico, text="Sintáctico")
        
        self.tree_sintactico = ttk.Treeview(
            self.tab_sintactico,
            columns=('Tipo', 'Mensaje', 'Línea', 'Columna'),
            show='headings',
            selectmode='browse'
        )
        
        columnas = [
            ('Tipo', 150, 'w'),
            ('Mensaje', 500, 'w'),
            ('Línea', 80, 'center'),
            ('Columna', 80, 'center')
        ]
        
        for col, width, anchor in columnas:
            self.tree_sintactico.heading(col, text=col)
            self.tree_sintactico.column(col, width=width, anchor=anchor)
        
        vsb = ttk.Scrollbar(self.tab_sintactico, orient="vertical", command=self.tree_sintactico.yview)
        hsb = ttk.Scrollbar(self.tab_sintactico, orient="horizontal", command=self.tree_sintactico.xview)
        self.tree_sintactico.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree_sintactico.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        self.tab_sintactico.grid_rowconfigure(0, weight=1)
        self.tab_sintactico.grid_columnconfigure(0, weight=1)
    
    def configurar_pestana_semantico(self):
        self.tab_semantico = tk.Frame(self.panel_resultados)
        self.panel_resultados.add(self.tab_semantico, text="Semántico")
        
        self.tree_semantico = ttk.Treeview(
            self.tab_semantico,
            columns=('Tipo', 'Mensaje', 'Línea', 'Columna'),
            show='headings',
            selectmode='browse'
        )
        
        columnas = [
            ('Tipo', 150, 'w'),
            ('Mensaje', 500, 'w'),
            ('Línea', 80, 'center'),
            ('Columna', 80, 'center')
        ]
        
        for col, width, anchor in columnas:
            self.tree_semantico.heading(col, text=col)
            self.tree_semantico.column(col, width=width, anchor=anchor)
        
        vsb = ttk.Scrollbar(self.tab_semantico, orient="vertical", command=self.tree_semantico.yview)
        hsb = ttk.Scrollbar(self.tab_semantico, orient="horizontal", command=self.tree_semantico.xview)
        self.tree_semantico.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree_semantico.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        self.tab_semantico.grid_rowconfigure(0, weight=1)
        self.tab_semantico.grid_columnconfigure(0, weight=1)
    
    def analizar_codigo(self):
        codigo = self.entrada_codigo.get("1.0", tk.END).strip()
        
        # Limpiar resultados anteriores
        for tree in [self.tree_tokens, self.tree_errores, self.tree_sintactico, self.tree_semantico]:
            tree.delete(*tree.get_children())
        
        # Análisis léxico
        tokens, errores = self.analizador_lexico.analizar(codigo)
        
        # Mostrar tokens
        for i, token in enumerate(tokens):
            self.tree_tokens.insert('', tk.END, values=(
                token.get('tipo', ''),
                token.get('valor', ''),
                token.get('linea', ''),
                token.get('columna', ''),
                i
            ))
        
        # Mostrar errores léxicos
        for error in errores:
            self.tree_errores.insert('', tk.END, values=(
                error.get('tipo', 'Error'),
                error.get('mensaje', ''),
                error.get('linea', ''),
                error.get('columna', ''),
                ''
            ))
        
        # Actualizar barra de estado
        self.label_tokens.config(text=f"Tokens: {len(tokens)}")
        self.label_errores.config(text=f"Errores: {len(errores)}")
        self.label_sintactico.config(text="Sintáctico: -")
        self.label_semantico.config(text="Semántico: -")
        
        return tokens, errores
    
    def analizar_sintactico(self):
        tokens, errores_lexicos = self.analizar_codigo()
        
        # Limpiar pestañas de análisis sintáctico y semántico
        self.tree_sintactico.delete(*self.tree_sintactico.get_children())
        self.tree_semantico.delete(*self.tree_semantico.get_children())
        
        if errores_lexicos:
            self.tree_sintactico.insert('', tk.END, values=(
                'Error',
                'No se puede realizar el análisis sintáctico con errores léxicos',
                '',
                ''
            ))
            self.label_sintactico.config(text="Sintáctico: Error léxico")
            self.label_semantico.config(text="Semántico: -")
            return
        
        # Realizar análisis sintáctico
        errores_sintacticos = self.analizador_sintactico.analizar(tokens)
        
        # Mostrar resultados
        if not errores_sintacticos:
            self.tree_sintactico.insert('', tk.END, values=(
                'Éxito',
                'El análisis sintáctico se completó sin errores',
                '',
                ''
            ))
            self.label_sintactico.config(text="Sintáctico: Correcto")
        else:
            for error in errores_sintacticos:
                self.tree_sintactico.insert('', tk.END, values=(
                    error.get('tipo', 'Error'),
                    error.get('mensaje', ''),
                    error.get('linea', ''),
                    error.get('columna', '')
                ))
            self.label_sintactico.config(text=f"Sintáctico: {len(errores_sintacticos)} errores")
    
    def analizar_semantico(self):
        tokens, errores_lexicos = self.analizar_codigo()
        
        # Limpiar pestaña de análisis semántico
        self.tree_semantico.delete(*self.tree_semantico.get_children())
        
        if errores_lexicos:
            self.tree_semantico.insert('', tk.END, values=(
                'Error',
                'No se puede realizar el análisis semántico con errores léxicos',
                '',
                ''
            ))
            self.label_semantico.config(text="Semántico: Error léxico")
            return
        
        # Realizar análisis sintáctico primero
        errores_sintacticos = self.analizador_sintactico.analizar(tokens)
        if errores_sintacticos:
            self.tree_semantico.insert('', tk.END, values=(
                'Error',
                'No se puede realizar el análisis semántico con errores sintácticos',
                '',
                ''
            ))
            self.label_semantico.config(text="Semántico: Error sintáctico")
            return
        
        # Realizar análisis semántico
        errores_semanticos = self.analizador_semantico.analizar(tokens)
        
        # Mostrar resultados
        if not errores_semanticos:
            self.tree_semantico.insert('', tk.END, values=(
                'Éxito',
                'El análisis semántico se completó sin errores',
                '',
                ''
            ))
            self.label_semantico.config(text="Semántico: Correcto")
        else:
            for error in errores_semanticos:
                self.tree_semantico.insert('', tk.END, values=(
                    error.get('tipo', 'Error'),
                    error.get('mensaje', ''),
                    error.get('linea', ''),
                    error.get('columna', '')
                ))
            self.label_semantico.config(text=f"Semántico: {len(errores_semanticos)} errores")