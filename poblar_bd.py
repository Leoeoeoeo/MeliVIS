import pandas as pd
import mysql.connector

# Rutas de los archivos Excel
ruta_poblacion_total = "BASE_CASO_PRATICA_VIS_20230424_3.xlsx"
ruta_uso_internet = "BASE_CASO_PRATICA_VIS_20230424_2.xlsx"
ruta_suscripciones_moviles = "BASE_CASO_PRATICA_VIS_20230424.xlsx"

# Configuración de conexión a la base de datos MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "MeliVIS"
}

# Función para leer y limpiar los datos
def leer_y_limpiar_excel(ruta, sheet_name, skiprows=3):
    """
    Lee y limpia el archivo Excel para asegurarse de que las columnas estén alineadas.
    """
    df = pd.read_excel(ruta, sheet_name=sheet_name, engine="openpyxl", skiprows=skiprows)

    df = df.dropna(subset=["Country Code"])
    return df

# Función para procesar los datos
def procesar_datos(df, columnas_a_eliminar, anio_inicio):
    df = df.drop(columns=columnas_a_eliminar, errors='ignore')

    df["Country Name"] = df["Country Name"].fillna("Desconocido") # Rellenar valores nulos en "Country Name" con "Desconocido"
    
    df = df.melt(id_vars=["Country Name", "Country Code"], var_name="Year", value_name="Value")

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df[df["Year"] >= anio_inicio]

    df.sort_values(by=["Country Code", "Year"], inplace=True)

    df["Value"] = (
        df.groupby("Country Code", group_keys=False)["Value"]
        .apply(lambda x: x.ffill().bfill().fillna(0)) # Rellenar valores faltantes: intermedios con el último valor conocido y previos con 0
    )

    return df.reset_index(drop=True)


# Función para insertar países
def insertar_paises(cursor, conexion, df):
    """
    Inserta países en la tabla Paises.
    """
    paises = df[["Country Name", "Country Code"]].drop_duplicates()
    for _, row in paises.iterrows():
        try:
            nombre_pais = row["Country Name"] if pd.notna(row["Country Name"]) else "Desconocido"
            cursor.execute("""
                INSERT IGNORE INTO Paises (Nombre, Codigo)
                VALUES (%s, %s)
            """, (nombre_pais, row["Country Code"]))
        except Exception as e:
            print(f"Error al insertar país: {row}. Error: {e}")
    conexion.commit()

# Función para obtener el ID del país por su código
def obtener_pais_id(cursor, codigo):
    """
    Obtiene el ID del país dado su código.
    """
    cursor.execute("SELECT id FROM Paises WHERE Codigo = %s", (codigo,))
    result = cursor.fetchone()
    return result[0] if result else None

# Función para insertar datos
def insertar_datos(cursor, conexion, tabla, df, columna_valor):
    """
    Inserta datos en una tabla MySQL.
    """
    for _, row in df.iterrows():
        try:
            pais_id = obtener_pais_id(cursor, row["Country Code"])
            if pais_id:
                cursor.execute(f"""
                    INSERT INTO {tabla} (PaisID, CodigoPais, Anio, {columna_valor})
                    VALUES (%s, %s, %s, %s)
                """, (pais_id, row["Country Code"], int(row["Year"]), float(row["Value"])))
            else:
                print(f"País no encontrado para código: {row['Country Code']}")
        except Exception as e:
            print(f"Error al insertar fila: {row}. Error: {e}")
    conexion.commit()

try:
    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor()

    poblacion_total = leer_y_limpiar_excel(ruta_poblacion_total, sheet_name="Data")
    uso_internet = leer_y_limpiar_excel(ruta_uso_internet, sheet_name="Data")
    suscripciones_moviles = leer_y_limpiar_excel(ruta_suscripciones_moviles, sheet_name="Data")

    poblacion_total_limpio = procesar_datos(
        poblacion_total,
        columnas_a_eliminar=["Indicator Name", "Indicator Code"],
        anio_inicio=1960
    )

    uso_internet_limpio = procesar_datos(
        uso_internet,
        columnas_a_eliminar=["Indicator Name", "Indicator Code"],
        anio_inicio=2000
    )

    suscripciones_moviles_limpio = procesar_datos(
        suscripciones_moviles,
        columnas_a_eliminar=["Indicator Name", "Indicator Code"],
        anio_inicio=2000
    )

    insertar_paises(cursor, conexion, poblacion_total)

    # Insertar datos en cada tabla
    insertar_datos(cursor, conexion, "PoblacionTotal", poblacion_total_limpio, "Valor")
    insertar_datos(cursor, conexion, "UsoInternet", uso_internet_limpio, "Porcentaje")
    insertar_datos(cursor, conexion, "SuscripcionesMoviles", suscripciones_moviles_limpio, "Suscripciones")

    print("Datos insertados correctamente.")

except mysql.connector.Error as e:
    print(f"Error al conectar o insertar en MySQL: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conexion' in locals():
        conexion.close()
