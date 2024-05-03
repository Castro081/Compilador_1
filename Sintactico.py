import re

class Sintactico:

    reglas_sintacticas = [

        r'<tipo_dato_A><ident><fin>', #1
        r'<tipo_dato_A><ident><igual><valor><fin>', #2
        r'<tipo_dato_A><ident><sep><ident><fin>', #3
        r'<cond><par_iz><ident><par_dr>', #4
        r'<tipo_dato_bucle><par_iz><ident><par_dr>', #5
        r'<cond><par_iz><ident><igual><ident><par_dr>', #6
        r'<cond><par_iz><ident><igual><valor><par_dr>', #7
        r'<cond><par_iz><valor><igual><ident><par_dr>', #8
        r'<tipo_dato_bucle><par_iz><ident><igual><ident><par_dr>', #9
        r'<tipo_dato_bucle><par_iz><ident><igual><valor><par_dr>', #10
        r'<tipo_dato_bucle><par_iz><valor><igual><ident><par_dr>', #11
        r'<tipo_dato_A><ident><igual><valor><sep><ident><igual><valor><fin>', #12
        r'<tipo_dato_A><ident><igual><valor><sep><ident><fin>', #13
        r'<tipo_dato_A><ident><sep><ident><igual><valor><fin>', #14
        r'<tipo_dato_A><ident><igual><ident><fin>' #15
    ]

    @staticmethod
    def abrir_resultado_lexico():
        try:
            with open('tokens.dhica', 'r') as file:
                return file.read()
        except FileNotFoundError:
            print('Error: No se encontró el archivo.')
        except Exception as e:
            print(f'Error al abrir el archivo: {e}')
        return None

    @staticmethod
    def tomar_informacion():
        contenido = Sintactico.abrir_resultado_lexico()
        if contenido:
            tokens = contenido.splitlines()
            resultado_linea = []
            for token in tokens:
                primera_palabra_tk = r'<(\w+)'
                linea = re.findall(primera_palabra_tk, token)
                linea = ''.join(f'<{tipo}>' for tipo in linea)
                resultado_linea.append(linea)
            return resultado_linea
        return []

    @staticmethod
    def procesar_informacion():
        resultado = Sintactico.tomar_informacion()
        resultados_sintacticos = []
        for idx, info in enumerate(resultado, start=1):
            if any(info.startswith(regla) for regla in Sintactico.reglas_sintacticas):
                resultados_sintacticos.append(f'Aceptada')
                print('Aceptada')
            else:
                resultados_sintacticos.append(f'Error de sintaxis: no cumple con ninguna regla sintáctica conocida.')
                print('Error')
        return resultados_sintacticos




resultado_sintactico = Sintactico.procesar_informacion()
print(resultado_sintactico)
