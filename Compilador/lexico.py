import re

class AnalizadorLexico:
    def __init__(self):
        self.patrones_tokens = [
            # Elementos a ignorar
            ('COMENTARIO', r'#.*', True),
            ('ESPACIO', r'[ \t]+', True),
            ('NUEVA_LINEA', r'\n', True),
            
            # Palabras reservadas
            ('IF', r'\bif\b'),
            ('ELIF', r'\belif\b'),
            ('ELSE', r'\belse\b'),
            ('WHILE', r'\bwhile\b'),
            ('FOR', r'\bfor\b'),
            ('IN', r'\bin\b'),
            ('DEF', r'\bdef\b'),
            ('RETURN', r'\breturn\b'),
            ('TRUE', r'\bTrue\b'),
            ('FALSE', r'\bFalse\b'),
            ('NONE', r'\bNone\b'),
            ('AND', r'\band\b'),
            ('OR', r'\bor\b'),
            ('NOT', r'\bnot\b'),
            
            # Operadores
            ('OPERADOR_ARITMETICO', r'\+|-|\*|\/|%|\*\*'),
            ('OPERADOR_COMPARACION', r'<=|>=|==|!=|<|>'),
            ('OPERADOR_ASIGNACION', r'='),
            ('OPERADOR_INCREMENTO', r'\+=|-=|\*=|\/='),
            ('DOS_PUNTOS', r':'),
            ('COMA', r','),
            ('PUNTO', r'\.'),
            
            # Delimitadores
            ('PARENTESIS_IZQ', r'\('),
            ('PARENTESIS_DER', r'\)'),
            ('LLAVE_IZQ', r'\{'),
            ('LLAVE_DER', r'\}'),
            ('CORCHETE_IZQ', r'\['),
            ('CORCHETE_DER', r'\]'),
            
            # Literales
            ('NUMERO', r'-?\d+\.?\d*([eE][+-]?\d+)?'),
            ('CADENA', r'\"(?:\\.|[^"\\])*\"|\'(?:\\.|[^\'\\])*\''),
            
            # Identificadores
            ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            
            # Error
            ('ERROR', r'.')
        ]
        
        self.regex = re.compile('|'.join(f'(?P<{nombre}>{patron})' for nombre, patron, *_ in self.patrones_tokens))
        self.ignorar = {nombre for nombre, _, *rest in self.patrones_tokens if rest and rest[0]}

    def analizar(self, codigo):
        tokens = []
        errores = []
        linea_actual = 1
        inicio_linea = 0
        indentacion_stack = [0]
        current_indent = 0
        prev_line = 1
        en_indentacion = True

        for match in self.regex.finditer(codigo):
            tipo = match.lastgroup
            valor = match.group()
            inicio = match.start()
            columna = inicio - inicio_linea + 1

            if tipo == 'NUEVA_LINEA':
                linea_actual += 1
                inicio_linea = match.end()
                en_indentacion = True
                current_indent = 0
                continue

            if tipo in self.ignorar:
                if en_indentacion and tipo == 'ESPACIO':
                    current_indent += len(valor)
                continue

            if tipo == 'ERROR':
                errores.append({
                    'tipo': 'Error Léxico',
                    'mensaje': f"Carácter inesperado: '{valor}'",
                    'linea': linea_actual,
                    'columna': columna
                })
                continue

            if en_indentacion and linea_actual != prev_line:
                self.procesar_indentacion(tokens, current_indent, indentacion_stack, linea_actual, columna, errores)
                prev_line = linea_actual
                en_indentacion = False

            tokens.append({
                'tipo': tipo,
                'valor': valor,
                'linea': linea_actual,
                'columna': columna
            })

        while indentacion_stack[-1] > 0:
            tokens.append({
                'tipo': 'DEDENT',
                'valor': '',
                'linea': linea_actual,
                'columna': 0
            })
            indentacion_stack.pop()

        tokens.append({
            'tipo': 'EOF',
            'valor': '',
            'linea': linea_actual,
            'columna': 0
        })

        return tokens, errores

    def procesar_indentacion(self, tokens, current_indent, stack, linea, columna, errores):
        last_indent = stack[-1]
        
        if current_indent > last_indent:
            stack.append(current_indent)
            tokens.append({
                'tipo': 'INDENT',
                'valor': '',
                'linea': linea,
                'columna': columna
            })
        elif current_indent < last_indent:
            while stack[-1] > current_indent and stack[-1] != 0:
                stack.pop()
                tokens.append({
                    'tipo': 'DEDENT',
                    'valor': '',
                    'linea': linea,
                    'columna': columna
                })
            if current_indent not in stack:
                errores.append({
                    'tipo': 'Error Léxico',
                    'mensaje': f"Indentación inconsistente en línea {linea}",
                    'linea': linea,
                    'columna': columna
                })