import re
import tkinter as tk
from Sintactico import Sintactico
import tkinter.messagebox as messagebox




class Analizador:
    def __init__(self, texto, salida_texto):
        self.texto = texto
        self.salida_texto = salida_texto

    tablas = {
    'Tabla_RW': {
        'tipo_dato_A': r'int',
        'tipo_dato_B': r'double',
        'tipo_dato_C': r'char',
        'tipo_dato_E': r'public',
        'tipo_dato_F': r'private',
        'cond': r'if',
        'tipo_dato_G': r'main',
        'tipo_dato_bucle': r'while'
    },

    'Tabla_signos': {
        'sep': r'\,', 
        'fin': r';',
        'igual': r'=',
        'resta' : r'-',
        'mayor' : r'>',
        'menor' : r'<',
        'par_iz': r'\(',
        'par_dr': r'\)',
        'llave_iz': r'\{',
        'llave_dr': r'\}'
        
    },

    'Tabla_identificador': {
        'ident': r'\b(?!(int|double|char|private|public|if|main|while)\b)\d*[a-zA-Z_]\w*\b'
    },
    'Tabla_numeros': {
        'valor': r'([.,]\d+)|(\d+[.,]\d+)|(\d+[.,]|\d+)'
    }
  }

    def validar_identificador(self, token):
        identificador_error = re.compile(r'[0-9]+[0-9a-zA-Z_]+')
        return identificador_error.search(token) is None
    
    def validar_identificador_especial(self, token):
        identificadores_error_especial = re.compile(r'\b[a-zA-Z_]*[$#%&][a-zA-Z_]*\b')
        return identificadores_error_especial.search(token) is None

    def validar_numero(self, token):
        numero_error = re.compile(r'^[.][0-9]+$|^[0-9]+[.]$|\b(\d+,\d+)\b|\b(\d+\.$)\b|\b(\d+,)\b')
        return numero_error.search(token) is not None

    def validar_palabra_similar_reservada(self, token):
        palabras_reservadas = ['int', 'double', 'char', 'public', 'private', 'if', 'main','while']
        return any(palabra.startswith(token.lower()) for palabra in palabras_reservadas)

    def validar_palabras_reservadas_consecutivas(self, linea):
        palabras_reservadas = ['int', 'double', 'char', 'public', 'private', 'if', 'main','while']
        tokens = linea.split()
        for i in range(len(tokens) - 1):
            token_actual = tokens[i].lower()
            token_siguiente = tokens[i + 1].lower()
            if token_actual in palabras_reservadas and token_siguiente in palabras_reservadas:
                return False
        return True


    def Token(self, texto):
        tokens = []
        texto_comentario = False
        for fila, linea in enumerate(texto.split('\n'), start=1):
            if '//' in linea or '--' in linea:
                continue

            if not texto_comentario:
                if '/*' in linea or '"""' in linea or "'''" in linea:
                    texto_comentario = True
                    continue

            if texto_comentario:
                if '*/' in linea or '"""' in linea or "'''" in linea:
                    texto_comentario = False
                continue
            
            for tabla, encontrar in self.tablas.items():
                for tipo, buscar_tabla in encontrar.items():
                    if tipo == 'ident':
                        buscar_tabla = r'\b(?!(int|double|char|private|public|if|main|while)\b)\d*[a-zA-Z_](\w|[$#%&])*\b'
                    for match in re.finditer(buscar_tabla, linea):
                        if tipo == 'sep' and match.group() == ',':
                            tokens.append(('sep', '","', fila, match.start() + 1))
                        elif tipo == 'end' or tipo == 'asig' or tipo == 'resta' or tipo == 'mayor' or tipo == 'menor':
                            tokens.append((tipo, match.group(), fila, match.start() + 1)) 
                        else:
                            tokens.append((tipo, match.group(), fila, match.start() + 1))

        return tokens


    def palabras_analizadas(self):
        texto = self.texto.get("1.0", tk.END)
        tokens = self.Token(texto)
        tokens.sort(key=lambda x: (x[2], x[3]))  
        tokens_str = ""
        linea_actual = 1
        tokens_linea_actual = []
        palabras_reservadas = ['int', 'double', 'char', 'public', 'private', 'if', 'main','while']  
        errores = []  
        for i in range(len(tokens)):
            token = tokens[i]
            if token[0] == 'valor' and self.validar_numero(token[1]):
                error = f'Error: El número  "{token[1]}" no es válido en la línea {token[2]}, columna {token[3]}'
                errores.append(error)
            elif token[0] == 'ident' and not self.validar_identificador(token[1]):
                error = f'Error: El identificador "{token[1]}" no es válido en la línea {token[2]}, columna {token[3]}'
                errores.append(error)
            elif token[0] == 'ident' and not self.validar_identificador_especial(token[1]):
                error = f'Error: El identificador "{token[1]}" no es válido en la línea {token[2]}, columna {token[3]}'
                errores.append(error)
            elif token[0] == 'ident' and self.validar_palabra_similar_reservada(token[1]):
                error = f'Error: EL "{token[1]}" se parece a una palabra reservada pero no coincide exactamente en la línea {token[2]}, columna {token[3]}'
                errores.append(error)
            elif i < len(tokens) - 1 and token[1] in palabras_reservadas and tokens[i + 1][1] in palabras_reservadas:
            
                if token[2] == tokens[i + 1][2] and token[3] + len(token[1]) + 1 == tokens[i + 1][3]:
                    error = f'Error: Palabra reservada consecutiva "{token[1]}" "{tokens[i + 1][1]}" en la línea {token[2]}, columna {token[3]}'
                    errores.append(error)
                        
        if errores:  
            tokens_str = ""
            for error in errores:
                tokens_str += error + '\n'
        else:  
            tokens_str = ""
            for token in tokens:
                if token[2] == linea_actual:
                    tokens_linea_actual.append(token)
                else:
                    linea_tokens = ' '.join([f'<{t[0]}, {t[1]}, {t[2]}, {t[3]}>' for t in tokens_linea_actual])
                    tokens_str += f'{linea_tokens}\n'
                    linea_actual = token[2]
                    tokens_linea_actual = [token]

            linea_tokens = ' '.join([f'<{t[0]}, {t[1]}, {t[2]}, {t[3]}>' for t in tokens_linea_actual])
            tokens_str += f'{linea_tokens}\n'
        
        
        return tokens_str.rstrip('\n')