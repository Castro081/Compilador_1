from tkinter import filedialog as fd
from tkinter import messagebox as mb

class BtArchivo:
    @staticmethod
    def limpiar(texto, salida_texto):
        texto.delete("1.0", "end")
        salida_texto.config(state="normal")  
        salida_texto.delete("1.0", "end")  
        salida_texto.config(state="disabled")
    

    @staticmethod
    def guardar(texto, salida_texto):
        contenido_texto = texto.get("1.0", "end").strip()
        contenido_salida = salida_texto.get("1.0", "end").strip()
        contenido_guardar = f"[texto]\n{contenido_texto}\n[texto_salida]\n{contenido_salida}"

        nombre_archivo = fd.asksaveasfilename(
            initialdir="",
            title="Guardar como",
            filetypes=(("Archivos de texto", "*.dhica"), ("Todos los archivos", "*.*")),
            defaultextension=".dhica"
        )
        if nombre_archivo != "":
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                archivo.write(contenido_guardar)
            mb.showinfo("Información", "El texto se guardó correctamente.")

    @staticmethod
    def cargar(texto, salida_texto):
        nombre_archivo = fd.askopenfilename(
            initialdir="",
            title="Seleccione un archivo",
            filetypes=(("Archivos de texto", "*.dhica"), ("Todos los archivos", "*.*"))
        )
        if nombre_archivo != "":
            with open(nombre_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()

                # Dividir el contenido en el área de texto y el área de salida
                inicio_texto = "[texto]"
                fin_texto = "[texto_salida]"
                if inicio_texto in contenido and fin_texto in contenido:
                    inicio_pos = contenido.index(inicio_texto) + len(inicio_texto)
                    fin_pos = contenido.index(fin_texto)

                    # Obtener el contenido para el área de texto y el área de salida
                    contenido_texto = contenido[inicio_pos:fin_pos].strip()
                    contenido_salida = contenido[fin_pos + len(fin_texto):].strip()

                    # Actualizar el contenido de los textfields
                    texto.delete("1.0", "end")
                    texto.insert("1.0", contenido_texto)

                    salida_texto.config(state="normal")
                    salida_texto.delete("1.0", "end")
                    salida_texto.insert("1.0", contenido_salida)
                    salida_texto.config(state="disabled")
                else:
                    mb.showerror("Error", "El archivo no tiene el formato esperado.")