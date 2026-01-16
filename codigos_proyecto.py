import json
import matplotlib.pyplot as plt
import numpy as np


#JSONS
#datos de disponibilidad y precios recopilados en las 30 MIPYMES visitadas(importar json)

with open("data/mipymes.json", "r" , encoding="utf-8") as f:
    datos_mipymes = json.load(f)




#datos de disponibilidad y precios recopilados en los anuncios de Revolico (importar json)

with open("data/productos_revolico.json", "r" , encoding="utf-8") as f:
    revolico_datos = json.load(f)




#importar json de productos del sitio A VER QUÉ SALE

with open("data/averquesale_por_producto.json", "r" , encoding="utf-8") as f:
    averquesale_datos = json.load(f)






#Para la realización del análisis usaremos las siguientes funciones que luego se implementarán
def calcular_porcentaje(parte, total):
    if total == 0:
        return 0
    return(parte/total)*100

def analizar_disponibilidad(lista_productos, fuentes_de_datos):
    resultados = {}
    for producto in lista_productos:
        producto_id = producto["id"]
        contador = 0
        for fuente in fuentes_de_datos:
            if fuente["productos"][str(producto_id)]["disponible"]:
                contador += 1
        total_fuentes = len(fuentes_de_datos)


        resultados[producto_id] = {
            "nombre": producto["nombre"],
            "disponibles":contador,
            "total": total_fuentes,
            "porcentaje":calcular_porcentaje(contador, len(fuentes_de_datos))}
    return resultados

def productos_no_disponibles(resultados_disponibilidad):
    productos_no = []
    for producto_id, datos in resultados_disponibilidad.items():
        if datos["disponibles"] == 0:
            productos_no.append(datos["nombre"])
    return productos_no


def calcular_promedio(lista):
    if len(lista) == 0:
        return 0
    return sum(lista) / len(lista)




#productos esenciales para adultos mayores que serán evaluados

productos = [
        {"id": 1, "nombre": "Paquete de arroz(1kg)", "categoría": "Alimentación"},
        {"id": 2, "nombre": "Avena instantánea", "categoría": "Alimentación"},
        {"id": 3, "nombre": "Paquete de pollo", "categoría": "Alimentación"},
        {"id": 4, "nombre": "Leche en caja(1lt)", "categoría": "Alimentación"},
        {"id": 5, "nombre": "Leche en polvo(1kg)", "categoría": "Alimentación"},
        {"id": 6, "nombre": "Cartón de huevos", "categoría": "Alimentación"},
        {"id": 7, "nombre": "Paquete de gelatina", "categoría": "Alimentación"},
        {"id": 8, "nombre": "Caja de cereal", "categoría": "Alimentación"},
        {"id": 9, "nombre": "Jabón", "categoría": "Higiene"},
        {"id": 10, "nombre": "Tubo de pasta dental", "categoría": "Higiene"},
        {"id": 11, "nombre": "Papel higiénico", "categoría": "Higiene"},
        {"id": 12, "nombre": "Bastón de apoyo", "categoría": "Movibilidad"},
        {"id": 13, "nombre": "Culeros geriátricos", "categoría": "Salud"},
        {"id": 14, "nombre": "Suplementos vitamínicos(Vitamina C)", "categoría": "Salud"},
        {"id": 15, "nombre": "Medicamentos para hipertensión(Lisinopril)", "categoría": "Salud"}
    ]
def mostrar_productos_esenciales():
    print(f"PRODUCTOS ESENCIALES DEFINIDOS: {len(productos)}")
    print("LISTA COMPLETA DE PRODUCTOS:")
    print("="*70)
    print("ID  | CATEGORÍA     | PRODUCTO")
    print("-"*70)

    for p in productos:
        print(f"{p['id']:3d} | {p['categoría']:13} | {p['nombre']}")
    PENSION_MINIMA = 3056
    print(f"PUNTO DE REFERENCIA: Pensión mínima = {PENSION_MINIMA:,} CUP")






#tabla de disponibilidad en mypimes
def tabla_mipymes():
    print("DISPONIBILIDAD EN MIPYMES")
    print("="*80)

    resultados_mipymes = analizar_disponibilidad(productos, datos_mipymes["mipymes"])

    print(f"\n {'PRODUCTO':44} {'DISPONIBLE EN':20} {'PORCENTAJE'}")
    print("-"*80)

    for producto_id in sorted(resultados_mipymes.keys()):
        datos = resultados_mipymes[producto_id]
        nombre = datos["nombre"][:44]
        disponible = f"{datos['disponibles']}/{datos['total']} MIPYMES"
        porcentaje = f"{datos['porcentaje']:.1f}%"

        print(f"{nombre:45} {disponible:20} {porcentaje}")

    print("-"*80)
    faltantes = productos_no_disponibles(resultados_mipymes)
    total_mipymes = len(datos_mipymes)

    print(f"PRODUCTOS DISPONIBLES: {len(productos) - len(faltantes)} / {len(productos)}")
    print(f"PRODUCTOS NO DISPONIBLES: {len(faltantes)}")




#Gráfico que muestra los productos que tienen disponibilidad alta, media y crítica
from matplotlib.patches import Patch

def grafico_mipymes(resultados_mipymes, datos_mipymes):

    plt.close("all")
    nombres = []
    porcentajes = []
    colores = []

    # recorrer resultados de disponibilidad
    for producto_id in sorted(resultados_mipymes.keys()):
        datos = resultados_mipymes[producto_id]
        nombres.append(datos["nombre"])
        porcentajes.append(datos["porcentaje"])

        if datos["porcentaje"] == 0:
            colores.append("red")
        elif datos["porcentaje"] < 50:
            colores.append("gold")
        else:
            colores.append("darkgreen")

    # crear figura
    fig = plt.figure(figsize=(12, 8))
    bars = plt.barh(nombres, porcentajes, color=colores)

    # etiquetas de porcentaje al lado de cada barra
    for bar, pct in zip(bars, porcentajes):
        if pct == 0:
            plt.text(1, bar.get_y() + bar.get_height()/2,
                     "0%", va="center", color="red", fontweight="bold")
        else:
            plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                     f"{pct:.1f}%", va="center", fontweight="bold")

    # título y ejes
    plt.title(f"DISPONIBILIDAD DE PRODUCTOS EN {len(datos_mipymes['mipymes'])} MIPYMES",
              fontsize=16, fontweight="bold", pad=20)
    plt.xlabel("PORCENTAJE DE MIPYMES QUE TIENEN EL PRODUCTO (%)", fontsize=12)
    plt.xlim(0, 105)

    # leyenda
    leyenda = [
        Patch(color="darkgreen", label="Alta disponibilidad (>=50%)"),
        Patch(color="gold", label="Baja disponibilidad (<50%)"),
        Patch(color="red", label="No disponibles (0%)")
    ]
    plt.legend(handles=leyenda, loc="lower right")

    plt.tight_layout()
    plt.show()





#tabla de precios promedio de los productos básicos obtenidos del scraping de Revolico, comparados con la pensión mínima de 3056 CUP
def tabla_revolico():

    pension_minima = 3056  # CUP
    filas = []

    for producto, anuncios in revolico_datos.items():
        precios = []
        for a in anuncios:
            if a.get("precio_cup"):
                nums = [float(x) for x in a["precio_cup"].split() if x.replace(".", "").isdigit()]
                if nums:
                    precios.append(nums[0])

        if precios:
            promedio = calcular_promedio(precios)
            unidades = pension_minima / promedio
            porcentaje = calcular_porcentaje(promedio, pension_minima)
            filas.append([producto, round(promedio, 2), round(unidades, 2), round(porcentaje, 2)])

    filas.sort(key=lambda x: x[3])

    print(f"{'Producto':<20}{'Precio promedio (CUP)':<25}{'Unidades con pensión mínima':<35}{'% de la pensión':<20}")
    print("-" * 96)
    for fila in filas:
        print(f"{fila[0]:<20}{fila[1]:<25}{fila[2]:<35}{fila[3]:<20}")






#gráfico que muestra el porcentaje de la pensión mínima de 3056 CUP que representa cada producto


def grafico_revolico():

    pension_minima = 3056  # CUP
    filas = []

    # construir filas directamente aquí
    for producto, anuncios in revolico_datos.items():
        precios = []
        for a in anuncios:
            if a.get("precio_cup"):
                nums = [float(x) for x in a["precio_cup"].split() if x.replace(".", "").isdigit()]
                if nums:
                    precios.append(nums[0])

        if precios:
            promedio = calcular_promedio(precios)
            unidades = pension_minima / promedio
            porcentaje = calcular_porcentaje(promedio, pension_minima)
            filas.append([producto, round(promedio, 2), round(unidades, 2), round(porcentaje, 2)])

    filas.sort(key=lambda x: x[3])

    # ahora graficar
    productos = [fila[0] for fila in filas]
    porcentajes = [fila[3] for fila in filas]

    plt.figure(figsize=(12, 6))
    plt.plot(productos, porcentajes, marker="o", linestyle="-", color="purple")

    plt.xticks(rotation=45, ha="right")
    plt.ylabel("% de la pensión mínima")
    plt.title("Porcentaje de la pensión mínima que representa cada producto")

    plt.axhline(100, color="red", linestyle="--", label="Pensión completa")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()







#gráfico de dispersión que permite ver qué productos están en cero unidades y cuáles tienen mayor accesibilidad

def grafico_accesibilidad():

    pension_minima = 3056
    filas = []

    # construir filas con producto, precio promedio y unidades
    for producto, anuncios in revolico_datos.items():
        precios = []
        for a in anuncios:
            if a.get("precio_cup"):
                nums = [float(x) for x in a["precio_cup"].split() if x.replace(".", "").isdigit()]
                if nums:
                    precios.append(nums[0])
        if precios:
            promedio = calcular_promedio(precios)
            unidades = pension_minima / promedio
            filas.append([producto, round(promedio, 2), round(unidades, 2)])

    # datos para el gráfico
    productos = [fila[0] for fila in filas]
    unidades = [fila[2] for fila in filas]

    plt.figure(figsize=(12, 6))
    plt.scatter(productos, unidades, color="darkred", s=100, alpha=0.8, edgecolors="black")

    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Unidades con pensión mínima")
    plt.title("Accesibilidad de productos con pensión mínima (3056 CUP)")
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    max_val = max(unidades)
    plt.yticks(np.arange(0, max_val+1, 1))  # paso de 1 en 1

    plt.tight_layout()
    plt.show()







#tabla que muestra el costo promedio de cada producto incluido en el archivo json (a ver que sale)
def tabla_averquesale():

    filas = []
    costo_total = 0

    print("Producto                       Promedio")
    print("-" * 43)

    for producto, anuncios in averquesale_datos.items():
        precios = []
        for anuncio in anuncios:
            precio = anuncio.get("precio_convertido", "").replace("CUP", "").strip()
            try:
                precios.append(float(precio))
            except:
                pass
        if precios:
            promedio = sum(precios) / len(precios)
            costo_total += promedio
            filas.append([producto, round(promedio, 2)])
            print(f"{producto.upper():30} {promedio:.2f} CUP")

    print("-" * 43)
    print(f"{'COSTO TOTAL TODOS':30} {costo_total:.2f} CUP")







#tabla de análisis comparativo entre el costo de la cesta básica (arroz, pollo, leche, pasta dental, papel higiénico) y la pensión mínima


def tabla_cesta_basica():

    pension = 3056
    cesta_basica = ["arroz", "pollo", "leche-caja-1lt", "jabon", "pasta-dental", "papel-higienico"]

    costo_total_cesta = 0
    print("Producto             Promedio")
    print("-" * 33)

    for producto in cesta_basica:
        if producto in averquesale_datos:
            valores = []
            for anuncio in averquesale_datos[producto]:
                precio = anuncio.get("precio_convertido", "").replace("CUP", "").strip()
                try:
                    valores.append(float(precio))
                except:
                    pass
            if valores:
                promedio = sum(valores) / len(valores)
                costo_total_cesta += promedio
                print(f"{producto.upper():20} {promedio:.2f} CUP")

    print("-" * 33)
    print(f"{'COSTO TOTAL CESTA':20} {costo_total_cesta:.2f} CUP")
    print("-" * 33)
    print(f"{'PENSIÓN MÍNIMA':20} {pension:.2f} CUP")
    print(f"{'RELACIÓN':20} {calcular_porcentaje(costo_total_cesta, pension):.2f}%")









#El siguiente gráfico circular muestra la proporción que representa cada producto dentro del costo total de la cesta básica


def grafico_cesta_basica():

    productos = ["ARROZ", "POLLO", "LECHE-CAJA-1LT", "JABON", "PASTA-DENTAL", "PAPEL-HIGIENICO"]
    valores = [736.93, 4110.47, 2050.00, 109.25, 250.00, 400.00]

    plt.figure(figsize=(6, 6))
    plt.pie(valores,
            labels=productos,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.85)
    plt.title("Distribución del costo de la cesta básica")
    plt.show()







#gráfico que muestra la comparación directa entre el costo total de la cesta y la pensión mínima

def grafico_cesta_vs_pension():

    costo_total_cesta = 8210.63
    pension = 3056

    plt.figure(figsize=(6, 6))
    plt.pie([costo_total_cesta, pension],
            labels=["Cesta Básica", "Pensión Mínima"],
            autopct="%1.1f%%",
            colors=["#ff9999", "#66b3ff"],
            startangle=90,
            wedgeprops={'width': 0.4})
    plt.title("Comparación: Cesta vs Pensión")
    plt.show()













