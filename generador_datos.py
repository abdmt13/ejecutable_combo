"""Genera datos de prueba en formato correo:password.

Las direcciones usan dominios reservados para ejemplos y no son cuentas reales.
"""

import secrets
import string
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# Dominios reservados para documentación y pruebas: no entregan correo.
PROVEEDORES = {
    "Gmail (prueba)": "gmail.example",
    "Hotmail (prueba)": "hotmail.example",
    "Outlook (prueba)": "outlook.example",
    "Yahoo (prueba)": "yahoo.example",
    "iCloud (prueba)": "icloud.example",
    "Proton Mail (prueba)": "proton.example",
    "Otro dominio de prueba": "correo.example",
}


def generar_password():
    """Crea una contraseña de longitud aleatoria (8–24) con letras y números ASCII."""
    longitud = secrets.randbelow(17) + 8
    caracteres = string.ascii_letters + string.digits
    return "".join(secrets.choice(caracteres) for _ in range(longitud))


def generar():
    proveedor = proveedor_var.get()
    try:
        cantidad = int(cantidad_var.get())
        if cantidad < 1 or cantidad > 10000:
            raise ValueError
    except ValueError:
        messagebox.showerror("Cantidad inválida", "Escribe un número entre 1 y 10 000.")
        return

    dominio = PROVEEDORES[proveedor]
    lineas = []
    passwords = set()
    for _ in range(cantidad):
        usuario = "usuario" + secrets.token_hex(5)
        password = generar_password()
        while password in passwords:
            password = generar_password()
        passwords.add(password)
        lineas.append(f"{usuario}@{dominio}:{password}")

    ruta = filedialog.asksaveasfilename(
        title="Guardar datos de prueba",
        defaultextension=".txt",
        initialfile="datos_de_prueba.txt",
        filetypes=[("Archivo de texto", "*.txt")],
    )
    if not ruta:
        return
    try:
        with open(ruta, "w", encoding="utf-8", newline="\n") as archivo:
            archivo.write("\n".join(lineas) + "\n")
    except OSError as error:
        messagebox.showerror("No se pudo guardar", str(error))
        return
    messagebox.showinfo(
        "Archivo creado",
        f"Se guardaron {cantidad} registros de prueba en:\n{ruta}\n\n"
        "Las direcciones usan dominios .example y no reciben correo.",
    )


ventana = tk.Tk()
ventana.title("Generador de datos de prueba")
ventana.resizable(False, False)

marco = ttk.Frame(ventana, padding=18)
marco.grid()

ttk.Label(marco, text="Proveedor de correo de prueba:").grid(row=0, column=0, sticky="w", pady=(0, 5))
proveedor_var = tk.StringVar(value="Gmail (prueba)")
ttk.Combobox(
    marco,
    textvariable=proveedor_var,
    values=list(PROVEEDORES),
    state="readonly",
    width=28,
).grid(row=1, column=0, sticky="ew", pady=(0, 14))

ttk.Label(marco, text="¿Cuántos registros quieres generar? (1–10 000)").grid(
    row=2, column=0, sticky="w", pady=(0, 5)
)
cantidad_var = tk.StringVar(value="10")
ttk.Entry(marco, textvariable=cantidad_var, width=12).grid(row=3, column=0, sticky="w", pady=(0, 14))

ttk.Label(
    marco,
    text="Formato: correo:contraseña\nLos dominios .example son solo para pruebas.",
).grid(row=4, column=0, sticky="w", pady=(0, 14))
ttk.Button(marco, text="Generar y guardar .txt", command=generar).grid(row=5, column=0, sticky="ew")

ventana.mainloop()
