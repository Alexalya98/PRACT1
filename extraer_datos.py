import requests
from bs4 import BeautifulSoup
import csv
import datetime

# Base URL de la página de IDESCAT con datos de salud
BASE_URL = "https://www.idescat.cat/indicadors/?id=basics&n=10380&lang=es&tema=salut&any={}"

# Función para obtener los datos de la web para un año específico
def obtener_datos(anio):
    url = BASE_URL.format(anio)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al acceder a la página para el año {anio}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar la tabla donde están los datos
    tabla = soup.find('table')
    if not tabla:
        print(f"No se encontró la tabla de datos para el año {anio}")
        return []
    
    datos = []
    for fila in tabla.find_all('tr')[1:]:  # Ignorar la primera fila (encabezados)
        columnas = fila.find_all('td')
        if len(columnas) >= 3:
            edad = columnas[0].text.strip()
            indicador = columnas[1].text.strip()
            valor = columnas[2].text.strip()
            datos.append([anio, edad, indicador, valor])
    
    return datos

# Función para guardar los datos en un archivo CSV
def guardar_csv(datos):
    nombre_archivo = "datos_idescat_1992_2022.csv"
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Año", "Edad", "Indicador", "Valor"])
        escritor.writerows(datos)
    print(f"Datos guardados en {nombre_archivo}")

# Ejecutar el scraping y guardar los datos para los años 1992-2022
datos_totales = []
for anio in range(1992, 2023):
    print(f"Obteniendo datos para el año {anio}...")
    datos_anio = obtener_datos(anio)
    if datos_anio:
        datos_totales.extend(datos_anio)

if datos_totales:
    guardar_csv(datos_totales)
else:
    print("No se pudieron obtener datos.")
