class AnalizadorSintactico:
    def __init__(self):
        self.errores = []
        self.tokens = []
        self.posicion = 0
    
    def analizar(self, tokens):
        self.errores = []
        self.tokens = tokens
        self.posicion = 0
        
        try:
            self.programa()
            if not self.fin() and self.actual()['tipo'] != 'EOF':
                token = self.actual()
                self.agregar_error(f"Token inesperado: {token['valor']}", token['linea'], token['columna'])
        except Exception as e:
            self.agregar_error(f"Error crítico: {str(e)}", 0, 0)
        
        return self.errores
    
    def programa(self):
        while not self.fin() and self.actual()['tipo'] != 'EOF':
            if self.comparar('INDENT') or self.comparar('DEDENT'):
                self.avanzar()
            else:
                self.declaracion()
    
    def declaracion(self):
        if self.comparar('IF'):
            self.estructura_if()
        elif self.comparar('WHILE'):
            self.estructura_while()
        elif self.comparar('FOR'):
            self.estructura_for()
        elif self.comparar('DEF'):
            self.declaracion_funcion()
        elif self.comparar('RETURN'):
            self.declaracion_return()
        elif self.comparar('IDENTIFICADOR') and self.mirar_adelante_tipo(1) == 'OPERADOR_ASIGNACION':
            self.asignacion()
        else:
            self.expresion()
    
    def estructura_if(self):
        self.consumir('IF', "Se esperaba 'if'")
        self.condicion()
        self.consumir('DOS_PUNTOS', "Se esperaba ':' después de if")
        
        if self.comparar('INDENT'):
            self.consumir('INDENT', "Se esperaba indentación")
            while not self.comparar('DEDENT') and not self.fin():
                self.declaracion()
            self.consumir('DEDENT', "Se esperaba fin de bloque")
        
        while self.comparar('ELIF'):
            self.consumir('ELIF', "Se esperaba 'elif'")
            self.condicion()
            self.consumir('DOS_PUNTOS', "Se esperaba ':' después de elif")
            
            if self.comparar('INDENT'):
                self.consumir('INDENT', "Se esperaba indentación")
                while not self.comparar('DEDENT') and not self.fin():
                    self.declaracion()
                self.consumir('DEDENT', "Se esperaba fin de bloque")
        
        if self.comparar('ELSE'):
            self.consumir('ELSE', "Se esperaba 'else'")
            self.consumir('DOS_PUNTOS', "Se esperaba ':' después de else")
            
            if self.comparar('INDENT'):
                self.consumir('INDENT', "Se esperaba indentación")
                while not self.comparar('DEDENT') and not self.fin():
                    self.declaracion()
                self.consumir('DEDENT', "Se esperaba fin de bloque")
    
    def condicion(self):
        if self.comparar('PARENTESIS_IZQ'):
            self.consumir('PARENTESIS_IZQ', "Se esperaba '('")
            self.expresion()
            self.consumir('PARENTESIS_DER', "Se esperaba ')'")
        else:
            self.expresion()
    
    def expresion(self):
        self.termino()
        while self.comparar('OPERADOR_ARITMETICO') or self.comparar('OPERADOR_COMPARACION') or \
              self.comparar('AND') or self.comparar('OR'):
            self.avanzar()
            self.termino()
    
    def termino(self):
        if self.comparar('NUMERO') or self.comparar('CADENA') or self.comparar('TRUE') or \
           self.comparar('FALSE') or self.comparar('NONE'):
            self.avanzar()
        elif self.comparar('IDENTIFICADOR'):
            self.llamada_funcion_o_identificador()
        elif self.comparar('PARENTESIS_IZQ'):
            self.consumir('PARENTESIS_IZQ', "Se esperaba '('")
            self.expresion()
            self.consumir('PARENTESIS_DER', "Se esperaba ')'")
        else:
            token = self.actual()
            self.agregar_error(
                f"Token inesperado: {token['tipo']} '{token['valor']}'",
                token['linea'], token['columna']
            )
            self.avanzar()
    
    def llamada_funcion_o_identificador(self):
        self.consumir('IDENTIFICADOR', "Se esperaba un identificador")
        if self.comparar('PARENTESIS_IZQ'):
            self.consumir('PARENTESIS_IZQ', "Se esperaba '('")
            self.argumentos()
            self.consumir('PARENTESIS_DER', "Se esperaba ')'")
    
    def argumentos(self):
        if not self.comparar('PARENTESIS_DER'):
            self.expresion()
            while self.comparar('COMA'):
                self.consumir('COMA', "Se esperaba ','")
                self.expresion()
    
    def asignacion(self):
        identificador = self.consumir('IDENTIFICADOR', "Se esperaba un identificador")
        self.consumir('OPERADOR_ASIGNACION', "Se esperaba '='")
        self.expresion()
    
    def estructura_while(self):
        self.consumir('WHILE', "Se esperaba 'while'")
        self.condicion()
        self.consumir('DOS_PUNTOS', "Se esperaba ':' después de while")
        
        if self.comparar('INDENT'):
            self.consumir('INDENT', "Se esperaba indentación")
            while not self.comparar('DEDENT') and not self.fin():
                self.declaracion()
            self.consumir('DEDENT', "Se esperaba fin de bloque")
    
    def estructura_for(self):
        self.consumir('FOR', "Se esperaba 'for'")
        self.consumir('IDENTIFICADOR', "Se esperaba variable después de 'for'")
        self.consumir('IN', "Se esperaba 'in' después de variable")
        # Permitir que la expresión sea una llamada a función como range(5)
        if self.comparar('IDENTIFICADOR'):
            self.llamada_funcion_o_identificador()
        else:
            self.expresion()
        self.consumir('DOS_PUNTOS', "Se esperaba ':' después de for")
        
        if self.comparar('INDENT'):
            self.consumir('INDENT', "Se esperaba indentación")
            while not self.comparar('DEDENT') and not self.fin():
                self.declaracion()
            self.consumir('DEDENT', "Se esperaba fin de bloque")
    
    def declaracion_funcion(self):
        self.consumir('DEF', "Se esperaba 'def'")
        self.consumir('IDENTIFICADOR', "Se esperaba nombre de función")
        self.consumir('PARENTESIS_IZQ', "Se esperaba '('")
        self.parametros()
        self.consumir('PARENTESIS_DER', "Se esperaba ')'")
        self.consumir('DOS_PUNTOS', "Se esperaba ':'")
        
        if self.comparar('INDENT'):
            self.consumir('INDENT', "Se esperaba indentación")
            while not self.comparar('DEDENT') and not self.fin():
                self.declaracion()
            self.consumir('DEDENT', "Se esperaba fin de bloque")
    
    def declaracion_return(self):
        self.consumir('RETURN', "Se esperaba 'return'")
        if not self.comparar('DOS_PUNTOS') and not self.comparar('DEDENT') and not self.fin():
            self.expresion()
    
    def parametros(self):
        if self.comparar('IDENTIFICADOR'):
            self.consumir('IDENTIFICADOR', "Se esperaba parámetro")
            while self.comparar('COMA'):
                self.consumir('COMA', "Se esperaba ','")
                self.consumir('IDENTIFICADOR', "Se esperaba parámetro")
    
    def actual(self):
        return self.tokens[self.posicion] if self.posicion < len(self.tokens) else {'tipo': 'EOF', 'valor': '', 'linea': 0, 'columna': 0}
    
    def avanzar(self):
        if not self.fin():
            self.posicion += 1
        return self.actual()
    
    def fin(self):
        return self.posicion >= len(self.tokens)
    
    def comparar(self, tipo):
        return not self.fin() and self.actual()['tipo'] == tipo
    
    def mirar_adelante_tipo(self, n):
        pos = self.posicion + n
        return self.tokens[pos]['tipo'] if pos < len(self.tokens) else None
    
    def consumir(self, tipo, mensaje):
        if self.comparar(tipo):
            return self.avanzar()
        else:
            token = self.actual()
            self.agregar_error(mensaje, token['linea'], token['columna'])
            self.avanzar()
            return None
    
    def agregar_error(self, mensaje, linea, columna):
        self.errores.append({
            'tipo': 'Error Sintáctico',
            'mensaje': mensaje,
            'linea': linea,
            'columna': columna
        })