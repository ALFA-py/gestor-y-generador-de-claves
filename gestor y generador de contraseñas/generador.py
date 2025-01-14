# ALFA, V1.0

import random
import string
import tkinter as tk
from tkinter import messagebox
import json
import os

archivo_json = "contraseñas.json"

def generar_contraseña():
    try:
        longitud = int(entry_longitud.get())
        if longitud < 6:
            messagebox.showwarning("Longitud insuficiente", "La longitud debe ser al menos de 6 caracteres.")
            return
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
        entry_resultado.config(state="normal")
        entry_resultado.delete(0, tk.END)
        entry_resultado.insert(0, contraseña)
        entry_resultado.config(state="readonly")
    except ValueError:
        messagebox.showerror("Entrada no válida", "Por favor, ingresa un número válido para la longitud.")

def guardar_contraseña_con_nombre():
    nombre = entry_nombre.get()
    contraseña = entry_resultado.get()
    if not nombre or not contraseña:
        messagebox.showwarning("Faltan campos", "Por favor, genera una contraseña y asigna un nombre antes de guardar.")
        return
    contraseñas_guardadas.append({"nombre": nombre, "contraseña": contraseña})
    guardar_contraseñas_en_archivo()
    actualizar_lista_contraseñas()

def actualizar_lista_contraseñas():
    lista_contraseñas.delete(0, tk.END)
    for contraseña_obj in contraseñas_guardadas:
        lista_contraseñas.insert(tk.END, f"{contraseña_obj['nombre']}: {contraseña_obj['contraseña']}")

def eliminar_contraseña():
    seleccion = lista_contraseñas.curselection()
    if seleccion:
        index = seleccion[0]
        contraseñas_guardadas.pop(index)
        guardar_contraseñas_en_archivo()
        actualizar_lista_contraseñas()
    else:
        messagebox.showwarning("No seleccionaste ninguna contraseña", "Por favor, selecciona una contraseña para eliminarla.")

def guardar_contraseñas_en_archivo():
    try:
        with open(archivo_json, 'w') as file:
            json.dump(contraseñas_guardadas, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

def cargar_contraseñas_desde_archivo():
    global contraseñas_guardadas
    try:
        if os.path.exists(archivo_json):
            with open(archivo_json, 'r') as file:
                contraseñas_guardadas = json.load(file)
                if not isinstance(contraseñas_guardadas, list):
                    contraseñas_guardadas = []
        else:
            contraseñas_guardadas = []
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
        contraseñas_guardadas = []
    actualizar_lista_contraseñas()

ventana = tk.Tk()
ventana.title("Generador de Contraseñas Seguras")
ventana.geometry("600x500")
ventana.config(bg="#000000")

contraseñas_guardadas = []

lista_contraseñas = tk.Listbox(ventana, font=("Arial", 12), width=40, height=5, bd=2, selectmode=tk.SINGLE, bg="#333", fg="yellow")
lista_contraseñas.pack(pady=10)

cargar_contraseñas_desde_archivo()

label_titulo = tk.Label(ventana, text="Generador y gestor de contraseñas", font=("Arial", 20, "bold"), bg="#000000", fg="yellow")
label_titulo.pack(pady=20)

label_longitud = tk.Label(ventana, text="Cuántos caracteres quieres para la contraseña:", font=("Arial", 12), bg="#000000", fg="white")
label_longitud.pack(pady=5)

entry_longitud = tk.Entry(ventana, font=("Arial", 14), width=10, justify="center", bd=2, fg="yellow", bg="#333")
entry_longitud.pack(pady=5)
entry_longitud.insert(0, "12")

label_nombre = tk.Label(ventana, text="Nombre de para qué será la contraseña:", font=("Arial", 12), bg="#000000", fg="white")
label_nombre.pack(pady=5)
entry_nombre = tk.Entry(ventana, font=("Arial", 14), width=30, justify="center", bd=2, fg="yellow", bg="#333")
entry_nombre.pack(pady=5)

boton_generar = tk.Button(ventana, text="Generar Contraseña", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", bd=0, relief="flat", width=20, height=2, command=generar_contraseña)
boton_generar.pack(pady=20)

boton_guardar = tk.Button(ventana, text="Guardar Contraseña", font=("Arial", 14, "bold"), bg="#00BFFF", fg="white", bd=0, relief="flat", width=20, height=2, command=guardar_contraseña_con_nombre)
boton_guardar.pack(pady=10)

label_resultado = tk.Label(ventana, text="Contraseña generada:", font=("Arial", 12), bg="#000000", fg="white")
label_resultado.pack(pady=5)

entry_resultado = tk.Entry(ventana, font=("Arial", 14), width=30, justify="center", bd=2, state="readonly", fg="green", bg="#333")
entry_resultado.pack(pady=5)

label_lista = tk.Label(ventana, text="Contraseñas guardadas:", font=("Arial", 12), bg="#000000", fg="white")
label_lista.pack(pady=5)

boton_eliminar = tk.Button(ventana, text="Eliminar Contraseña", font=("Arial", 12), bg="#FF5733", fg="white", bd=0, relief="flat", width=20, height=2, command=eliminar_contraseña)
boton_eliminar.pack(pady=10)

ventana.mainloop()
