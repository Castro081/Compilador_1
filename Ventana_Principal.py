import tkinter as tk
from tkinter import Toplevel, scrolledtext as st
from tkinter import Menu
from tkinter import ttk
from Analizador_IDE import Analizador
from Sintactico import Sintactico
from Semantico import AnalizadorSemantico
from Bt_Archivo import BtArchivo
import tkinter.messagebox as messagebox
import os


class IDE:
    def __init__(self):
        self.bt_archivo = BtArchivo()
        self.ventana = tk.Tk()
        self.ventana.title("Analizador")
        self.agregar_menu()
        self.ventana.columnconfigure(1, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        self.nombre_archivo = "tokens.dhica"
        if not os.path.exists(self.nombre_archivo):
            open(self.nombre_archivo, 'w', encoding="utf-8").close()

        # Área de texto
        self.texto = st.ScrolledText(self.ventana, width=80, height=20, wrap=tk.WORD, borderwidth=2, relief="sunken")
        self.texto.grid(column=1, row=0, padx=(0, 10), pady=10, sticky='nsew')

        # Área de texto de salida
        self.salida_label = tk.Label(self.ventana, text="Salida", font=("Arial", 12))
        self.salida_label.grid(column=0, row=1, padx=(15, 0), pady=(0, 15), sticky='nw')
        self.salida_texto = st.ScrolledText(self.ventana, width=80, height=10, wrap=tk.WORD, borderwidth=2, relief="sunken")
        self.salida_texto.grid(column=1, row=1, padx=(0, 10), pady=(0, 10), sticky='nsew')
        self.salida_texto.config(state="disabled")
        self.ventana.update_idletasks()

        # Centrar la ventana 
        x = (self.ventana.winfo_screenwidth() - self.ventana.winfo_reqwidth()) / 2
        y = (self.ventana.winfo_screenheight() - self.ventana.winfo_reqheight()) / 2
        self.ventana.geometry("+%d+%d" % (x, y))

        self.token = Analizador(self.texto, self.salida_texto) 
        self.ventana.mainloop()

    def agregar_menu(self):
        menubar1 = Menu(self.ventana)
        self.ventana.config(menu=menubar1)
        opciones1 = Menu(menubar1, tearoff=0)
        opciones1.add_command(label="Guardar Texto", command=lambda: BtArchivo.guardar(self.texto, self.salida_texto))
        opciones1.add_command(label="Cargar Texto", command=lambda: BtArchivo.cargar(self.texto, self.salida_texto))
        opciones1.add_separator()
        opciones1.add_command(label="Salir", command=self.salir)
        menubar1.add_cascade(label="Archivo", menu=opciones1)
        menubar1.add_command(label="Limpiar", command=lambda: BtArchivo.limpiar(self.texto, self.salida_texto))
        menubar1.add_command(label="Analizar", command=lambda: self.analizar())
        menubar1.add_command(label="Sintactico", command=lambda: self.Sintactico())
        menubar1.add_command(label="Semántico", command=lambda: self.Semantico())

    def salir(self):
        self.ventana.destroy()

    def Sintactico(self):
        # lugar para imprimir los valores del sintactico 
            resultado_sintactico = Sintactico.procesar_informacion()  # Obtener resultados del análisis sintáctico
            for mensaje in resultado_sintactico:
                # Mostrar mensaje donde desees
                if mensaje.startswith('Error de sintaxis'):
                    messagebox.showinfo('Error de sintaxis', mensaje)
                    # Eliminar contenido del área de salida_texto
                    self.salida_texto.config(state="normal")
                    self.salida_texto.delete("1.0", tk.END)
                    self.salida_texto.config(state="disabled")
                elif mensaje == 'Aceptada':
                    messagebox.showinfo('Cadena Aceptada', 'La cadena ha sido aceptada.')
    
    def obtener_texto(self):
        texto_a_analizar = self.texto.get("1.0", tk.END)  # Obtener el texto del área de texto
        return texto_a_analizar
        
    def mostrar_tabla_simbolos(self, simbolos):
        self.salida_texto.config(state="normal")
        self.salida_texto.delete("1.0", tk.END)
        self.salida_texto.insert(tk.END, "Tabla de Símbolos".center(80) + "\n")
        self.salida_texto.insert(tk.END, f"{'ID'.center(20)}{'Tipo'.center(20)}{'Valor'.center(20)}{'Scope'.center(20)}\n")
        self.salida_texto.insert(tk.END, "-"*80 + "\n")
        
        for simbolo in simbolos:
            id_text = simbolo['Identificador'].center(20)
            tipo_text = simbolo['Tipo'].center(20)
            valor = simbolo['Valor'] if simbolo['Valor'] is not None else 'N/A'
            valor_text = str(valor).center(20)
            scope_text = str(simbolo['Scope']).center(20)
            self.salida_texto.insert(tk.END, f"{id_text}{tipo_text}{valor_text}{scope_text}\n")
        
        self.salida_texto.config(state="disabled")

    def Semantico(self):
        texto_a_analizar = self.obtener_texto()
        if texto_a_analizar.strip():
            analizador_semantico = AnalizadorSemantico()
            lineas = texto_a_analizar.split('\n')
            analizador_semantico.analizar_semantica(lineas)
            analizador_semantico.imprimir_tabla_simbolos()
            if analizador_semantico.errores:
                messagebox.showerror('Errores Semánticos', '\n'.join(analizador_semantico.errores))
            elif analizador_semantico.advertencias:
                messagebox.showwarning('Advertencias Semánticas', '\n'.join(analizador_semantico.advertencias))
            else:
                messagebox.showinfo('Análisis Semántico Exitoso', 'El análisis semántico se completó correctamente sin errores ni advertencias.')
                self.mostrar_tabla_simbolos(analizador_semantico.tabla_simbolos)
        else:
            messagebox.showwarning('Análisis Semántico', 'No hay texto para analizar.')

    def analizar(self):
        tokens_analizados = self.token.palabras_analizadas()
        open(self.nombre_archivo, 'w').close() # Limpiar archivo

        # Escribir los tokens en el archivo
        with open(self.nombre_archivo, 'w', encoding="utf-8") as file:
            file.write(tokens_analizados)
    
        self.salida_texto.config(state="normal")
        self.salida_texto.delete("1.0", tk.END) 
        self.salida_texto.insert(tk.END, tokens_analizados)
        self.salida_texto.config(state="disabled")
        self.salida_texto.update_idletasks() 


    def limpiar(self):
        self.bt_archivo.limpiar(self.texto, self.salida_texto)

if __name__ == "__main__":
    IDE()
