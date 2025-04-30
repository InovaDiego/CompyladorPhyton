class AnalizadorSemantico:
    def __init__(self):
        self.errores = []
        self.tabla_simbolos = [{}]  # Lista de diccionarios para ámbitos
        self.funciones = {}  # Almacena funciones y sus parámetros
        self.posicion = 0
        self.tokens = []

    def analizar(self, tokens):
        self.errores = []
        self.tabla_simbolos = [{}]  
        self.funciones = {}
        self.posicion = 0
        self.tokens = tokens
        
        try:
            self.programa()
        except Exception as e:
            self.agregar_error(f"Error crítico: {str(e)}", 0, 0)
        
        return self.errores
    
    def programa(self):
        while not self.fin() and self.actual()['tipo'] != 'EOF':
            if self.comparar('INDENT'):
                self.tabla_simbolos.append({})
                self.avanzar()
            elif self.comparar('DEDENT'):
                self.tabla_simbolos.pop()
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
        self.consumir('IF')
        self.condicion()
        self.consumir('DOS_PUNTOS')
        if self.comparar('INDENT'):
            self.tabla_simbolos.append({})
            self.consumir('INDENT')
            while not self.comparar('DEDENT') and not self.fin():
                self.declaracion()
            self.consumir('DEDENT')
            self.tabla_simbolos.pop()
        
        while self.comparar('ELIF'):
            self.consumir('ELIF')
            self.condicion()
            self.consumir('DOS_PUNTOS')
            if self.comparar('INDENT'):
                self.tabla_simbolos.append({})
                self.consumir('INDENT')
                while not self.comparar('DEDENT') and not self.fin():
                    self.declaracion()
                self.consumir('DEDENT')
                self.tabla_simbolos.pop()
        
        if self.comparar('ELSE'):
            self.consumir('ELSE')
            self.consumir('DOS_PUNTOS')
            if self.comparar('INDENT'):
                self.tabla_simbolos.append({})
                self.consumir('INDENT')
                while not self.comparar('DEDENT') and not self.fin():
                    self.declaracion()
                self.consumir('DEDENT')
                self.tabla_simbolos.pop()
    
    def condicion(self):
        if self.comparar('PARENTESIS_IZQ'):
            self.consumir('PARENTESIS_IZQ')
            self.expresion()
            self.consumir('PARENTESIS_DER')
        else:
            self.expresion()
    
    def expresion(self):
        tipo = self.termino()
        while self.comparar('OPERADOR_ARITMETICO') or self.comparar('OPERADOR_COMPARACION'):
            op = self.avanzar()['valor']
            tipo_derecho = self.termino()
            # Solo reportar error si ambos tipos son conocidos e incompatibles
            if tipo != 'unknown' and tipo_derecho != 'unknown' and tipo != tipo_derecho:
                self.agregar_error(f"Incompatibilidad de tipos: {tipo} y {tipo_derecho} con operador {op}", 
                                self.actual()['linea'], self.actual()['columna'])
        return tipo
    
    def termino(self):
        if self.comparar('NUMERO'):
            self.avanzar()
            return 'number'
        elif self.comparar('CADENA'):
            self.avanzar()
            return 'string'
        elif self.comparar('IDENTIFICADOR'):
            identificador = self.actual()['valor']
            self.avanzar()
            if self.comparar('PARENTESIS_IZQ'):
                self.consumir('PARENTESIS_IZQ')
                self.argumentos()
                self.consumir('PARENTESIS_DER')
                if identificador not in self.funciones:
                    self.agregar_error(f"Función '{identificador}' no definida", 
                                     self.actual()['linea'], self.actual()['columna'])
                    return 'unknown'
                return 'unknown'  
            if not self.buscar_simbolo(identificador):
                self.agregar_error(f"Variable '{identificador}' no definida", 
                                 self.actual()['linea'], self.actual()['columna'])
                return 'unknown'
            return self.buscar_simbolo(identificador).get('tipo', 'unknown')
        elif self.comparar('TRUE') or self.comparar('FALSE'):
            self.avanzar()
            return 'boolean'
        elif self.comparar('NONE'):
            self.avanzar()
            return 'none'
        elif self.comparar('PARENTESIS_IZQ'):
            self.consumir('PARENTESIS_IZQ')
            tipo = self.expresion()
            self.consumir('PARENTESIS_DER')
            return tipo
        else:
            token = self.actual()
            self.agregar_error(f"Token inesperado en expresión: {token['valor']}", 
                             token['linea'], token['columna'])
            self.avanzar()
            return 'unknown'
    
    def argumentos(self):
        if not self.comparar('PARENTESIS_DER'):
            self.expresion()
            while self.comparar('COMA'):
                self.consumir('COMA')
                self.expresion()
    
    def asignacion(self):
        identificador = self.consumir('IDENTIFICADOR')['valor']
        self.consumir('OPERADOR_ASIGNACION')
        tipo = self.expresion()
        # Siempre agregar el símbolo, incluso si el tipo es 'unknown'
        self.agregar_simbolo(identificador, {'tipo': tipo if tipo != 'unknown' else 'number'})
    
    def estructura_while(self):
        self.consumir('WHILE')
        self.condicion()
        self.consumir('DOS_PUNTOS')
        if self.comparar('INDENT'):
            self.tabla_simbolos.append({})
            self.consumir('INDENT')
            while not self.comparar('DEDENT') and not self.fin():
                self.declaracion()
            self.consumir('DEDENT')
            self.tabla_simbolos.pop()
    
    def estructura_for(self):
        self.consumir('FOR')
        var = self.consumir('IDENTIFICADOR')['valor']
        self.consumir('IN')
        self.expresion()
        self.consumir('DOS_PUNTOS')
        self.agregar_simbolo(var, {'tipo': 'unknown'})
        if self.comparar('INDENT'):
            self.tabla_simbolos.append({})
            self.consumir('INDENT')
            while not self.comparar('DEDENT') and not self.fin():
                self.declaracion()
            self.consumir('DEDENT')
            self.tabla_simbolos.pop()
    
    def declaracion_funcion(self):
        self.consumir('DEF')
        nombre = self.consumir('IDENTIFICADOR')['valor']
        self.consumir('PARENTESIS_IZQ')
        params = self.parametros()  
        self.consumir('PARENTESIS_DER')
        self.consumir('DOS_PUNTOS')
        
        if nombre in self.funciones:
            self.agregar_error(f"Función '{nombre}' ya definida", 
                             self.actual()['linea'], self.actual()['columna'])
        else:
            self.funciones[nombre] = {'parametros': params}
        
        self.tabla_simbolos.append({})
        for param in params:
            self.agregar_simbolo(param, {'tipo': 'unknown'})
        
        if self.comparar('INDENT'):
            self.consumir('INDENT')
            while not self.comparar('DEDENT') and not self.fin():
                self.declaracion()
            self.consumir('DEDENT')
            self.tabla_simbolos.pop()
    
    def declaracion_return(self):
        self.consumir('RETURN')
        if not self.comparar('DOS_PUNTOS') and not self.comparar('DEDENT') and not self.fin():
            self.expresion()
    
    def parametros(self):
        params = []
        while self.comparar('IDENTIFICADOR'):
            params.append(self.consumir('IDENTIFICADOR')['valor'])
            if self.comparar('COMA'):
                self.consumir('COMA')
            else:
                break
        return params
    
    def agregar_simbolo(self, nombre, info):
        self.tabla_simbolos[-1][nombre] = info
    
    def buscar_simbolo(self, nombre):
        # Buscar en todos los ámbitos desde el más interno
        for ambito in reversed(self.tabla_simbolos):
            if nombre in ambito:
                return ambito[nombre]
        # Si no se encuentra, no marcar error inmediatamente (podría ser una función)
        return {'tipo': 'unknown'}
        
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
    
    def consumir(self, tipo):
        if self.comparar(tipo):
            return self.avanzar()
        else:
            token = self.actual()
            self.agregar_error(f"Se esperaba {tipo}, se encontró {token['tipo']}", 
                             token['linea'], token['columna'])
            self.avanzar()
            return None
    
    def agregar_error(self, mensaje, linea, columna):
        self.errores.append({
            'tipo': 'Error Semántico',
            'mensaje': mensaje,
            'linea': linea,
            'columna': columna
        })