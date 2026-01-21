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
            if str(producto_id) in fuente["productos"]:
                if fuente["productos"][str(producto_id)]["disponible"]:
                    contador += 1
        total_fuentes = len(fuentes_de_datos)
        porcentaje = (contador / total_fuentes) * 100 if total_fuentes > 0 else 0
        resultados[producto_id] = {
            "nombre": producto["nombre"],
            "disponibles": contador,
            "total": total_fuentes,
            "porcentaje": porcentaje
        }
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


    productos_mipymes = [p for p in productos if str(p["id"]) in datos_mipymes["mipymes"][0]["productos"]]

    resultados_mipymes = analizar_disponibilidad(productos_mipymes, datos_mipymes["mipymes"])

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
    print(f"PRODUCTOS DISPONIBLES: {len(productos_mipymes) - len(faltantes)} / {len(productos_mipymes)}")
    print(f"PRODUCTOS NO DISPONIBLES: {len(faltantes)}")















#Gráfico que muestra los productos que tienen disponibilidad alta, media y crítica


def grafico_anillo_mipymes():
    productos_mipymes = [p for p in productos if str(p["id"]) in datos_mipymes["mipymes"][0]["productos"]]
    resultados_mipymes = analizar_disponibilidad(productos_mipymes, datos_mipymes["mipymes"])


    grandes = []
    medianos = []
    pequeños = []
    otros_valor = 0
    otros_nombres = []

    for producto_id, datos in resultados_mipymes.items():
        nombre = datos["nombre"]
        porcentaje = datos["porcentaje"]
        if porcentaje < 5:
            otros_valor += porcentaje
            otros_nombres.append(nombre)
        elif nombre.lower().startswith("leche en polvo"):
            medianos.insert(len(medianos)//2, (nombre, porcentaje))
        elif porcentaje >= 10:
            grandes.append((nombre, porcentaje))
        else:
            medianos.append((nombre, porcentaje))

    if otros_valor > 0:
        pequeños.append(("Otros", otros_valor))


    nombres = []
    valores = []
    for g, m in zip(grandes, medianos):
        nombres.append(g[0]); valores.append(g[1])
        nombres.append(m[0]); valores.append(m[1])
    for g in grandes[len(medianos):]:
        nombres.append(g[0]); valores.append(g[1])
    for m in medianos[len(grandes):]:
        nombres.append(m[0]); valores.append(m[1])
    for p in pequeños:
        nombres.append(p[0]); valores.append(p[1])


    print("\nLos productos con disponibilidad menor al 5% han sido agrupados como 'Otros'.")
    if otros_nombres:
        print("Productos agrupados en 'Otros':")
        for nombre in otros_nombres:
            print(f" - {nombre}")

    colores = plt.cm.tab20.colors[:len(nombres)]

    fig, ax = plt.subplots(figsize=(9,9))
    wedges, texts, autotexts = ax.pie(
        valores,
        labels=nombres,
        autopct="%1.1f%%",
        startangle=135,
        colors=colores,
        wedgeprops=dict(width=0.3, edgecolor='white'),
        pctdistance=0.65,
        labeldistance=1.05
    )

    plt.text(0, 0, "Total: 13 productos", ha="center", va="center", fontsize=12, weight="bold")
    plt.title("Disponibilidad en MIPYMES", fontsize=14)
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


def grafico_barras_revolico():
    pension_minima = 3056
    nombres = []
    porcentajes = []

    for producto, ofertas in revolico_datos.items():
        precios = [float(oferta["precio_cup"].split()[0]) for oferta in ofertas]
        promedio = sum(precios) / len(precios)
        porcentaje_pension = (promedio / pension_minima) * 100
        nombres.append(producto)
        porcentajes.append(porcentaje_pension)


    colores = plt.cm.tab20.colors[:len(nombres)]

    fig, ax = plt.subplots(figsize=(10,6))
    barras = ax.bar(nombres, porcentajes, color=colores, edgecolor="black")

    for barra, valor in zip(barras, porcentajes):
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.5,
                f"{valor:.1f}%", ha="center", va="bottom", fontsize=9)

    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Porcentaje de la pensión mínima (%)")
    plt.title("Porcentaje de la pensión mínima de 3056 CUP que representa cada producto en Revolico")
    plt.tight_layout()
    plt.show()










#gráfico de dispersión que permite ver qué productos están en cero unidades y cuáles tienen mayor accesibilidad

def grafico_accesibilidad():

    pension_minima = 3056
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
            filas.append([producto, round(promedio, 2), round(unidades, 2)])


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

def tabla_cesta_basica_mensual():
    pension = 3056
    cesta_basica = {
        "arroz": 3,              # 3 paquetes de 1kg (~7 lb)
        "pollo": 1,              # 1 paquete (nota: puede variar según consumo)
        "leche-caja-1lt": 3,     # 3 cajas de 1lt
        "jabon": 2,              # 2 unidades
        "pasta-dental": 1,       # 1 tubo
        "papel-higienico": 1     # 1 paquete
    }

    costo_total_cesta = 0
    print("Producto             Promedio (CUP)   Cantidad mínima   Costo mensual (CUP)")
    print("-" * 70)

    for producto, cantidad in cesta_basica.items():
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
                costo_producto = promedio * cantidad
                costo_total_cesta += costo_producto
                print(f"{producto.upper():20} {promedio:10.2f} CUP   {cantidad:<15} {costo_producto:10.2f} CUP")

    print("-" * 70)
    print(f"{'COSTO TOTAL CESTA':20} {costo_total_cesta:.2f} CUP")
    print("-" * 70)
    print(f"{'PENSIÓN MÍNIMA':20} {pension:.2f} CUP")
    print(f"{'RELACIÓN':20} {calcular_porcentaje(costo_total_cesta, pension):.2f}%")









#El siguiente gráfico circular muestra la proporción que representa cada producto dentro del costo total de la cesta básica



def grafico_cesta_basica_mensual():
    pension = 3056


    arroz = 736.93 * 3
    pollo = 4110.47 * 1
    leche_caja = 2017.20 * 3
    jabon = 109.25 * 2
    pasta_dental = 625.70 * 1
    papel_higienico = 611.08 * 1

    productos = {
        "Arroz (3kg)": arroz,
        "Pollo (1 paquete)": pollo,
        "Leche caja 1lt (3)": leche_caja,
        "Jabón (2)": jabon,
        "Pasta dental": pasta_dental,
        "Papel higiénico": papel_higienico
    }


    costo_total = sum(productos.values())

    fig, ax = plt.subplots(figsize=(8,8))
    ax.pie(
        productos.values(),
        labels=productos.keys(),
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Distribución del costo mensual de la cesta básica", fontsize=14)
    plt.show()









#gráfico que muestra la comparación directa entre el costo total de la cesta y la pensión mínima


def grafico_brecha_pension_vs_cesta():
    pension = 3056
    costo_cesta = 13828.15
    brecha = costo_cesta - pension
    porcentaje_pension = pension / costo_cesta * 100
    porcentaje_brecha = brecha / costo_cesta * 100

    fig, ax = plt.subplots(figsize=(10,4))
    fig.patch.set_facecolor('#f5f5f5')

    ax.hlines(y=1, xmin=0, xmax=costo_cesta, colors="black", linestyles="--", linewidth=3)
    ax.barh(y=1, width=pension, height=0.15, color="dodgerblue")

    ax.text(pension/2, 0.85, f"{pension:.0f} CUP ({porcentaje_pension:.1f}%)",
            ha="center", fontsize=11, color="black", fontweight="bold")

    ax.text(pension + brecha/2, 1.05, f"Faltan {brecha:.0f} CUP ({porcentaje_brecha:.1f}%)",
            ha="center", fontsize=12, color="darkred", fontweight="bold")

    ax.text(pension + brecha/2, 0.7, "BRECHA GIGANTE",
            ha="center", fontsize=13, color="firebrick", fontweight="bold")

    ax.set_xlim(0, costo_cesta * 1.1)
    ax.set_ylim(0.6, 1.4)
    ax.axis("off")
    plt.title("Puente roto: pensión mínima vs costo de la cesta básica",
              fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.show()
















