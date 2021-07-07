import gestor
import tkinter as tk
from tkinter import ttk

mejorPolitica = ""
costoMenor = 99999999999999999999999999
# Metodos


def btnSimularClick():
    cleanTable(treeResolucion)
    politicaSeleccionada = comboPolitica.get()
    stock = int(cajaParamStockInicial.get())
    dias = int(cajaParamCantDias.get())
    desde = int(cajaParamMostarDesde.get())
    hasta = int(cajaParamIteraciones.get())+desde
    # Segundo control, si no selecciono alguna politica, se desabilita el boton
    if politicaSeleccionada == "":
        botonSimular["state"] = "disabled"
        return
    insertarFila(treeResolucion, gestor.empezarSimulacion(
        politicaSeleccionada, stock), 0)
    for i in range(1, dias):
        filaSimulada = gestor.calcularSiguienteFila()
        if i >= desde and i < hasta:
            insertarFila(treeResolucion, filaSimulada, i)
    insertarFila(treeResolucion, gestor.calcularSiguienteFila(), dias)
    temp = gestor.toHistorial()
    temp[1] = stock
    insertarFila(treeHistorial, temp, -1)
    evaluarResultado(temp)


def evaluarResultado(v):
    global costoMenor
    global mejorPolitica
    if v[3] < costoMenor:
        costoMenor = v[3]
        mejorPolitica = v[0]
    actualizarResultado()


def actualizarResultado():
    lblResultadoPolitica["text"] = mejorPolitica
    lblMenorCosto["text"] = costoMenor


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
# Interacciones y objetos
# Parametros adicionales:
cajaParamCantDias = tk.Entry(p1, width=10)
cajaParamCantDias.insert(0, 360)
lblParamStockInicial = tk.Label(p1, text="Cantidad de Dias")
cajaParamCantDias.place(x=175, y=10)
lblParamStockInicial.place(x=50, y=10)

cajaParamStockInicial = tk.Entry(p1, width=10)
cajaParamStockInicial.insert(0, 20)
lblParamStockInicial = tk.Label(p1, text="Stock Inicial")
cajaParamStockInicial.place(x=375, y=10)
lblParamStockInicial.place(x=275, y=10)

cajaParamMostarDesde = tk.Entry(p1, width=10)
cajaParamMostarDesde.insert(0, 0)
lblParamMostarDesde = tk.Label(p1, text="Mostrar desde:")
cajaParamMostarDesde.place(x=790, y=10)
lblParamMostarDesde.place(x=675, y=10)

cajaParamIteraciones = tk.Entry(p1, width=10)
cajaParamIteraciones.insert(0, 360)
lblParamIteraciones = tk.Label(p1, text="cantidad a mostrar:")
cajaParamIteraciones.place(x=1010, y=10)
lblParamIteraciones.place(x=870, y=10)

botonSimular = tk.Button(p1, text="Simular", padx=10,
                         pady=5, command=btnSimularClick, state="disabled")
botonSimular.place(x=1100, y=10)

lblPolitica = tk.Label(p1, text="Politica: ")
lblPolitica.place(x=425, y=10)
comboPolitica = ttk.Combobox(p1, state="readonly", postcommand=habilitarBoton)
comboPolitica.place(x=500, y=12)
comboPolitica["values"] = gestor.cargarPoliticas()
# Treeview Resolucion del ejercicio
headerMonteCarlo = [" Dia ", "RND Demanda", "Demanda", "Stock",
                    "Dia pedido reposicion", "RND Demora", "Demora",
                    "Dia Restock", "AC Demanda(P.B.)",
                    "Costo Almacenamiento", "Costo Faltante",
                    "Costo Adquisicion", "Costo Total DIA",
                    "AC Costo", "PROM costoPorDia"]
treeResolucion = ttk.Treeview(p1, height=29, column=[
                              f"#{cantidad}" for cantidad in range(1, len(headerMonteCarlo) + 1)], show='headings')
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

# Pestaña 2
# Resultados:
lblMejorPolitica = tk.Label(p2, text="Mejor politica:")
lblResultadoPolitica = tk.Label(p2)
lblCosto = tk.Label(p2, text="Costo:")
lblMenorCosto = tk.Label(p2)
lblMejorPolitica.place(x=100, y=20)
lblResultadoPolitica.place(x=225, y=20)
lblCosto.place(x=400, y=20)
lblMenorCosto.place(x=450, y=20)

# tabla de historial
headerResultadosPrevios = [
    "   Politica   ", "Stock Inicial", "Dias simulados", "Promedio costo por dia"]
treeHistorial = ttk.Treeview(p2, height=29, column=[f"#{cantidad}" for cantidad in range(
    0, len(headerResultadosPrevios)+1)], show='headings')
treeHistorial.place(x=300, y=50)

for i in range(len(headerResultadosPrevios)):
    treeHistorial.column("#" + str(i + 1), anchor=tk.CENTER,
                         width=100, minwidth=len(headerResultadosPrevios[i]) * 8 + 5)
    treeHistorial.heading("#" + str(i + 1), text=headerResultadosPrevios[i])
vsbp2 = ttk.Scrollbar(p2, orient="vertical", command=treeHistorial.yview)
vsbp2.pack(side='right', fill='y')
treeHistorial.configure(yscrollcommand=vsbp2.set)


# Añadimos Pestañas al window
nb.add(p1, text="Ejercicio")
nb.add(p2, text="Historial Simulaciones")
miWindow.mainloop()
