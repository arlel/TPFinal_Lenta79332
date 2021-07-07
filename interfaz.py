import gestor
import tkinter as tk
from tkinter import ttk


# Metodos
def btnSimularClick():
    cleanTable(treeResolucion)
    politicaSeleccionada = comboPolitica.get()
    # Segundo control, si no selecciono alguna politica, se desabilita el boton
    if politicaSeleccionada == "":
        botonSimular["state"] = "disabled"
        return
    insertarFila(treeResolucion, gestor.empezarSimulacion(politicaSeleccionada), 0)
    for i in range(1, 361):
        insertarFila(treeResolucion, gestor.calcularSiguienteFila(), i)


def habilitarBoton():
    botonSimular["state"] = "normal"


def cleanTable(tabla):
    tabla.delete(*tabla.get_children())


def insertarFila(treeview, fila, n):
    treeview.insert(parent='', index='end', text=str(n), values=fila)


# Interfaz
miWindow = tk.Tk()  # Creacion de la ventana contenedora
miWindow.title("Ejercicio 19 - Lenta 79332")
miWindow.geometry("1200x700")
miWindow.resizable(False, False)
# Pestaña
nb = ttk.Notebook(miWindow)
nb.pack(fill='both', expand='yes')

# Creamos Pestañas
p1 = ttk.Frame(nb)
p2 = ttk.Frame(nb)

# Pestaña 1
# Interacciones
botonSimular = tk.Button(p1, text="Simular", padx=10, pady=5, command=btnSimularClick, state="disabled")
botonSimular.place(x=550, y=10)

comboPolitica = ttk.Combobox(p1, state="readonly", postcommand=habilitarBoton)
comboPolitica.place(x=350, y=15)
comboPolitica["values"] = gestor.cargarPoliticas()
# Treeview Resolucion del ejercicio
headerMonteCarlo = ["Dia", "RND Demanda", "Demanda", "Stock",
                    "Dia pedido reposicion", "RND Demora", "Demora",
                    "Dia Restock", "AC Demanda(P.B.)",
                    "Costo Almacenamiento", "Costo Faltante",
                    "Costo Adquisicion", "Costo Total DIA",
                    "AC Costo", "PROM costoPorDia"]
treeResolucion = ttk.Treeview(p1, height=29, column=[f"#{cantidad}" for cantidad in range(1, len(headerMonteCarlo) + 1)]
                              , show='headings')
treeResolucion.place(x=15, y=50)

for i in range(len(headerMonteCarlo)):
    treeResolucion.column("#" + str(i + 1), anchor=tk.CENTER, width=77, minwidth=len(headerMonteCarlo[i]) * 8 + 5,
                          stretch=True)
    treeResolucion.heading("#" + str(i + 1), text=headerMonteCarlo[i])
vsb = ttk.Scrollbar(p1, orient="vertical", command=treeResolucion.yview)
vsb.pack(side='right', fill='y')
treeResolucion.configure(yscrollcommand=vsb.set)
vsb = ttk.Scrollbar(p1, orient="horizontal", command=treeResolucion.xview)
vsb.pack(side='bottom', fill='x')
treeResolucion.configure(xscrollcommand=vsb.set)

# Añadimos Pestañas al window
nb.add(p1, text="Ejercicio")
nb.add(p2, text="Resultados previos")
miWindow.mainloop()
