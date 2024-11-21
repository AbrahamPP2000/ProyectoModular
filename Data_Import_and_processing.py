import csv
import subprocess
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from Expert_System import ExpertSystem


# # Ruta de la carpeta con los archivos CSV
# folder = "C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV"
#
# # Lista todos los archivos en la carpeta
# files = os.listdir(folder)


# Funciones básicas

def update_dollar_price(cursor):
    # Actualización del precio del dólar cada vez que se ejecuta el programa

    # Fecha y hora actuales
    current_date = datetime.now()
    # Formateo de la fecha en el formato: Año-Mes-Día
    formatted_date = current_date.strftime("%Y-%m-%d")

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
            global exchange_rate
            exchange_rate = price_element.text
            print("Actualizando precio del dólar...")
            dollar_price_query = (f"UPDATE gestion_de_lotes.dolar SET Fecha = '{formatted_date}', "
                                   f"PrecioEnPesos = {exchange_rate} LIMIT 1")
            cursor.execute(dollar_price_query)
            connection.commit()

            dollar_file_route = r'C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Dolar.csv'
            try:
                # Leer el archivo CSV y almacenar las filas
                with open(dollar_file_route, mode='r', newline='') as csv_file:
                    reader_csv = csv.reader(csv_file)
                    rows = list(reader_csv)  # Convertir el contenido a una lista para modificarlo

                # Modificar la primera fila con los nuevos datos
                rows[1] = [formatted_date, exchange_rate]  # Modifica la fila 1 (índice 0 suele ser el encabezado)
    
                # Escribir el archivo CSV con las filas actualizadas
                with open(dollar_file_route, mode='w', newline='') as csv_file:
                    writer_csv = csv.writer(csv_file)
                    writer_csv.writerows(rows)  # Sobrescribir el archivo con las filas modificadas
                print("Precio del dólar actualizado con éxito en la base de datos y en el CSV.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
        else:
            print("No se pudo encontrar el tipo de cambio en la página.")
    else:
        print(f"Error al acceder a la página: {response.status_code}")


def sum_of_settled_amounts(cursor):
    query = "SELECT SUM(PrecioTotal) FROM Gestion_de_lotes.Lotes WHERE Estatus = 'Comprado'"
    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener el resultado de la suma
    result = cursor.fetchone()

    print(f"Resultado bruto: {result}")
    formatted_result = f"${result[0]:,.2f}"
    # Imprimir el resultado
    print(f"La suma de los importes es: {formatted_result}\n")
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def sum_of_payments_for_lots_to_be_sold(cursor):
    query = "SELECT SUM(CantidadAbonada) FROM Gestion_de_lotes.Abonos"
    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener el resultado de la suma
    result = cursor.fetchone()

    print(f"Resultado bruto: {result}")
    formatted_result = f"${result[0]:,.2f}"
    # Imprimir el resultado
    print(f"La suma de los abonos es: {formatted_result}")
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)
##################################### 21/11/24
def client_consultation(cursor):
    query = "SELECT Nombre FROM Gestion_de_lotes.Clientes"
    cursor.execute(query)
    info = cursor.fetchall()
    for row in info:
        print(row)
    pass
#####################################

def lot_consultation(cursor):
    # Preguntar por el número de lote y de manzana del lote.
    lot_number = input("Introduzca el número de lote: ")
    block_number = input("Ahora introduzca el número de la manzana en la que se ubica: ")
    # Mostrar la información correspondiente.
    query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE NoManzana = " + block_number + " and NoLote = " + lot_number
    cursor.execute(query)
    info = cursor.fetchall()
    for row in info:
        print(row)
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def info_adjustment(cursor):
    df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Lotes.csv")
    print(df)
    for _, row in df.iterrows():
        sql = """INSERT INTO Gestion_de_lotes.Lotes (NoManzana, NoLote, Direccion, MtsCuadrados, CostoMetroCuadrado,
        PrecioTotal, Estatus) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, tuple(row))
        connection.commit()
    subprocess.call("cls", shell=True)


def lot_purchase(cursor, rule_system):
    print("¿Cuál lote se quiere comprar?")
    print("Lista de lotes disponibles:\n")
    query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE Estatus = 'Disponible'"
    cursor.execute(query)
    info = cursor.fetchall()
    columns = cursor.column_names
    column_width = []

    for index, column in enumerate(columns):
        max_width = max(len(str(fila[index])) for fila in info) if info else 0
        column_width.append(max(max_width, len(column)))

    for index, column in enumerate(columns):
        print(column.ljust(column_width[index]), end = "\t")
    print()

    for row in info:
        for index, data in enumerate(row):
            print(str(data).ljust(column_width[index]), end = "\t")
        print()


    # After displaying the lots, ask for input and use the expert system
    no_manzana = int(input("Introduzca el número de manzana: "))
    no_lote = int(input("Introduzca el número de lote: "))

    # Fetch lot details from the database
    query = (f"SELECT MtsCuadrados, CostoMetroCuadrado, PrecioTotal FROM Gestion_de_lotes.Lotes WHERE NoManzana = "
             f"{no_manzana} AND NoLote = {no_lote}")
    cursor.execute(query)
    lot_details = cursor.fetchone()

    if lot_details:
        mts_cuadrados, costo_metro_cuadrado, precio_total = lot_details
        recommendation = rule_system.recommend_action(no_manzana, no_lote, mts_cuadrados, costo_metro_cuadrado,
                                                      precio_total)
        print("\nRecomendación del sistema experto:")
        print(recommendation)
    else:
        print("Lote no encontrado.")

    # # Imprimir los nombres de las columnas
    # print("\t".join(columnas))  # Usamos '\t' para separar por tabulación
    # # Imprimir las filas de la tabla sin paréntesis ni comas
    # for fila in info:
    #     fila_sin_comas = "\t".join(map(str, fila))  # Convertimos a cadena y separamos por tabulación
    #     print(fila_sin_comas)
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def balance_consultation(cursor):
    print("---------Consulta de saldo--------")
    lot_number = input("Introduzca el número de lote: ")
    block_number = input("Ahora introduzca el número de la manzana en la que se ubica: ")
    query = ("SELECT Saldo FROM Gestion_de_lotes.Abonos WHERE NoManzana = " + block_number + " and NoLote = " +
                lot_number + " and NoAbono = (SELECT MAX(NoAbono) FROM Gestion_de_lotes.Abonos WHERE NoManzana = " +
                block_number + " and NoLote = " + lot_number + ")")
    cursor.execute(query)
    balance = cursor.fetchone()
    print("El saldo del lote número " + lot_number + " de la manzana " + block_number + " es: $" + balance[0])
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)

def main_menu(cursor):
    rule_system = ExpertSystem(float(exchange_rate))
    rule_system.train_model(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Lotes.csv")

    while True:
        print("\n\nIniciar la compra de lote: (1)")
        print("Consultar un lote: (2)")
        print("Consultar la sumatoria de los importes finiquitados: (3)")
        print("Consultar la sumatoria de los abonos de los lotes en proceso de compra: (4)")
        print("Consultar el saldo de un lote: (5)")
        print("Consultar los datos de un cliente: (6)")
        print("Salir (Cualquier tecla)\n")
        election = input("Seleccione la operación que quiera realizar: ")
        if election == "1":
            lot_purchase(cursor, rule_system)
            subprocess.call("cls", shell=True)
        elif election == "2":
            lot_consultation(cursor)
            subprocess.call("cls", shell=True)
        elif election == "3":
            sum_of_settled_amounts(cursor)
            subprocess.call("cls", shell=True)
        elif election == "4":
            sum_of_payments_for_lots_to_be_sold(cursor)
            subprocess.call("cls", shell=True)
        elif election == "5":
            balance_consultation(cursor)
            subprocess.call("cls", shell=True)
        elif election == "6":
            client_consultation(cursor)
            subprocess.call("cls", shell=True)
        else:
            break


# Conectar a la base de datos MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='gestion_de_lotes',
        user='root',
        password='mysql24$^ui(yuAs'
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # ajuste_de_informacion(cursor)
        update_dollar_price(cursor)
        main_menu(cursor)

        # Confirmar los cambios en la base de datos
        connection.commit()
        cursor.close()
        connection.close()
        print("Conexión a MySQL cerrada")

except Error as e:
    print("(1)Error al conectar a MySQL", e)
