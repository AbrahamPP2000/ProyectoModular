# import chardet
#
# # Abrir el archivo en modo binario para detectar la codificación
# with open(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Clientes.csv", 'rb') as file:
#     raw_data = file.read()
#     result = chardet.detect(raw_data)
#     encoding = result['encoding']
#
# print(f"La codificación detectada es: {encoding}")

# import pandas as pd

# Leer el archivo CSV con la codificación original
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Abonos.csv", encoding='ascii')
# print(df)
# # Guardar el archivo CSV con la nueva codificación
# df.to_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\AbonosASCII.csv", encoding='ascii', index=False)

import requests
from bs4 import BeautifulSoup

# URL de Google Finance para el tipo de cambio USD/MXN
url = "https://www.google.com/finance/quote/USD-MXN"

# Hacemos una solicitud GET a la página
response = requests.get(url)

# Verificamos que la solicitud fue exitosa
if response.status_code == 200:
    # Parseamos el contenido HTML de la página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraemos el valor del tipo de cambio usando el selector adecuado
    price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})

    if price_element:
        # Obtenemos el texto del elemento
        exchange_rate = price_element.text
        print(f"El tipo de cambio actual de USD a MXN es: {exchange_rate}")
    else:
        print("No se pudo encontrar el tipo de cambio en la página.")
else:
    print(f"Error al acceder a la página: {response.status_code}")

from datetime import datetime

# Obtener la fecha y hora actuales
fecha_actual = datetime.now()

# # Formatear la fecha en el formato: Día-Mes-Año Hora:Minuto:Segundo
# fecha_formateada = fecha_actual.strftime("%d-%m-%Y %H:%M:%S")

# Formatear la fecha en el formato: Año-Mes-Día
fecha_formateada = fecha_actual.strftime("%Y-%d-%m")

# Mostrar la fecha formateada
print("Fecha formateada:", fecha_formateada)

# Leer el archivo CSV con pandas

# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Lotes.csv") # Ya importado
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Balance.csv")
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Clientes.csv") # Ya importado
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Compras.csv") # Ya importado
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Dolar.csv")
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Abonos.csv") # Ya importado
# print(df)
# Crear una consulta SQL para insertar los datos
# for _, row in df.iterrows():
# sql = """INSERT INTO Gestion_de_lotes.Lotes (NoManzana, NoLote, Direccion, MtsCuadrados)  # Ya importado
#          VALUES (%s, %s, %s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Clientes (IdCliente, Nombre, Domicilio, Telefono) # Ya importado
#          VALUES (%s, %s, %s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Dolar (Fecha, Pasivos, PatrimonioNeto, Activos)
#          VALUES (%s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Compras (NoManzana, NoLote, CostoPorMetroCuadrado, ImporteTotal, Fecha, IdCliente, FormaDePago) # Ya importado
#          VALUES (%s, %s, %s, %s, %s, %s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Balance (Fecha, Pasivos, PatrimonioNeto, Activos)
#          VALUES (%s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Abonos (Fecha, NoManzana, NoLote, NoAbono, CantidadAbonada, NoRecibo, Saldo) # Ya importado
#          VALUES (%s, %s, %s, %s, %s, %s, %s)"""

# cursor.execute(sql, tuple(row))
# cursor.execute("delete from Gestion_de_lotes.Balance where IdBalance = 1 ")

# Consulta de datos en una tabla.
# consulta = "select * from Gestion_de_lotes.Abonos"
# cursor.execute(consulta)
# info = cursor.fetchall()
# for registro in info:
#     print(registro)


# Obtención de un resultado a partir de una operación
# consulta = "SELECT SUM(ImporteTotal) FROM Gestion_de_lotes.Compras"
# # Ejecutar la consulta
# cursor.execute(consulta)
#
# # Obtener el resultado de la suma
# resultado = cursor.fetchone()
#
# # Imprimir el resultado
# print(f"La suma de los importes es: {resultado[0]}")
