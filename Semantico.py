class AnalizadorSemantico:
    def __init__(self):
        self.ambitos = []
        self.ambito_global = {}  
        self.tabla_simbolos = []
        self.errores = []
        self.advertencias = []
        self.tipos_validos = ["int", "double", "float", "char", "string", "boolean"]
        self.id_ambito_actual = 0

    def entrar_scope(self):
        self.ambitos.append({})
        self.id_ambito_actual += 1

    def salir_scope(self):
        if self.ambitos: 
            self.ambitos.pop()
            self.id_ambito_actual -= 1  

    def obtener_scope_actual(self):             
        return self.id_ambito_actual if self.ambitos else 0

    def agregar_simbolo(self, ident, tipo, fila):
        ambito = self.ambitos[-1] if self.ambitos else self.ambito_global
        if not self.ambitos and 'this' not in self.ambito_global:
            self.ambito_global['this'] = {}
        if ident == "this":
            self.errores.append(f"Error en la línea {fila}: 'this' no se puede declarar como una variable.")
            return False
        if ident in ambito:
            self.errores.append(f"Error de unicidad en la línea {fila}: El identificador '{ident}' ya ha sido declarado en este ámbito.")
            return False
        ambito[ident] = {'tipo': tipo, 'declarada': True, 'valor': None}
        if not self.ambitos:
            self.ambito_global['this'][ident] = {'tipo': tipo, 'declarada': True, 'valor': None}
        self.tabla_simbolos.append({
            "Identificador": ident,
            "Tipo": tipo,
            "Valor": None,  
            "Scope": self.id_ambito_actual,
            "Linea": fila
        })

    def asignar_simbolo(self, ident, valor, fila):
        valor_convertido = int(valor) if valor.isdigit() else valor
        encontrado = False

        if ident.startswith('this.'):
            variable = ident.split('.')[1]
            # Actualizar el valor en el ámbito global
            if variable in self.ambito_global['this']:
                self.ambito_global['this'][variable]['valor'] = valor_convertido
                encontrado = True
            else:
                self.errores.append(f"Error en línea {fila}: Variable '{variable}' no declarada bajo 'this'.")
                return

            # Actualizar la tabla 
            for simbolo in self.tabla_simbolos:
                if simbolo['Identificador'] == variable:
                    simbolo['Valor'] = valor_convertido

        else:
            # Buscar y actualizar la variable en el ámbito actual
            for ambito in reversed(self.ambitos):
                if ident in ambito:
                    ambito[ident]['valor'] = valor_convertido
                    encontrado = True
                    break

            if not encontrado and ident in self.ambito_global:
                self.ambito_global[ident]['valor'] = valor_convertido
                encontrado = True

            if encontrado:
                # Actualizar la tabla de símbolos
                for simbolo in self.tabla_simbolos:
                    if simbolo['Identificador'] == ident:
                        simbolo['Valor'] = valor_convertido
                        break
                else:
                    # Agregar a la tabla si no se encontró
                    self.tabla_simbolos.append({
                        'Identificador': ident,
                        'Tipo': type(valor_convertido).__name__,
                        'Valor': valor_convertido,
                        'Scope': self.obtener_scope_actual(),
                        'Linea': fila
                    })
            else:
                self.errores.append(f"Error en línea {fila}: Variable '{ident}' no declarada.")


    def analizar_semantica(self, lineas):
        valores_asignados = {}  # Para rastrear los valores asignados a las variables
        for numero_linea, linea in enumerate(lineas, start=1):
            tokens = linea.strip().split()
            if not tokens:
                continue
            elif tokens[0] == '{':
                self.entrar_scope()
            elif tokens[0] == '}':
                self.salir_scope()
            elif tokens[0] in self.tipos_validos and len(tokens) > 1:
                ident = tokens[1].strip(';')
                self.agregar_simbolo(ident, tokens[0], numero_linea)
            elif "=" in linea:
                partes = linea.split('=')
                if len(partes) == 2:
                    ident = partes[0].strip()
                    valor = partes[1].strip(';').strip()
                    self.asignar_simbolo(ident, valor, numero_linea)
                    valores_asignados[ident] = valor  # Guardar los valores asignados


    def imprimir_errores_y_advertencias(self):
        if self.errores:
            print("ERRORES:")
            for error in self.errores:
                print(error)
        if self.advertencias:
            print("ADVERTENCIAS:")
            for advertencia in self.advertencias:
                print(advertencia)
        if not self.errores and not self.advertencias:
            print("No se encontraron errores ni advertencias.")


    def imprimir_tabla_simbolos(self):
        print("Tabla de Símbolos:")
        for simbolo in self.tabla_simbolos:
            ident = simbolo.get('Identificador', 'Desconocido')
            tipo = simbolo.get('Tipo', 'Desconocido')
            valor = simbolo.get('Valor', 'N/A')
            scope_id = simbolo.get('Scope', 'N/A')
            linea = simbolo.get('Linea', 'Desconocido')
            print(f"{ident} - {tipo} - Valor: {valor} - Scope ID: {scope_id} - Linea: {linea}")
