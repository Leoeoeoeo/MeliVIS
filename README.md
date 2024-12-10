# Desafío Meli VIS

Para poder hacer uso de la base de datos `MeliVIS_export.sql` donde se encuentran todas la tablas y datos ya cargados se debe ingresar el siguiente comando:
```
mysql -u root -p MeliVIS < MeliVIS_export.sql
```

## Esquema de la BD
### Tablas

Esta base de datos contiene 4 tablas principales que contienen toda la información necesaria de los Dataset entregados:

| Tabla | Descripción |
| --- | --- |
| paises | Contiene la información que clasifica a los paises. |
| poblaciontotal | Contiene los datos del tercer excel |
| suscripcionesmoviles | Contiene los datos del primer excel |
| usointernet | Contiene los datos del segundo excel |

Cada tabla contiene los siguientes atributos:

**Paises:**

| Campo | Type | Descripción |
| --- | --- | --- |
| id | int | Identificador único del país. |
| Nombre | varchar(255) | Nombre completo del país. |
| Codigo | char(3) | Código identificador del país. |

**PoblacionTotal:**

| Campo | Type | Descripción |
| --- | --- | --- |
| id | int | Identificador único de la fila. |
| PaisID | int | Id del Pais. |
| CodigoPais | char(3) | Código identificador del país. |
| Anio | int | Año del dato. |
| Valor | bigint | Dato de la población total. |

**UsoInternet:**

| Campo | Type | Descripción |
| --- | --- | --- |
| id | int | Identificador único de la fila. |
| PaisID | int | Id del Pais. |
| CodigoPais | char(3) | Código identificador del país. |
| Anio | int | Año del dato. |
| Porcentaje | float | Dato del porcentaje de la población que hace uso de Internet. |

**SuscripcionesMoviles:**

| Campo | Type | Descripción |
| --- | --- | --- |
| id | int | Identificador único de la fila. |
| PaisID | int | Id del Pais. |
| CodigoPais | char(3) | Código identificador del país. |
| Anio | int | Año del dato. |
| Suscripciones | bigint | Dato de cantidad de suscripciones moviles. |


## Querys de Uso

### Query para ver por Año y País los indicadores de % personas que usan internet, suscripciones a telefonía celular móvil y población total.

```
SELECT 
    p.Nombre AS Pais,
    p.Codigo AS CodigoPais,
    pt.Anio AS Anio,
    pt.Valor AS PoblacionTotal,
    ui.Porcentaje AS PorcentajeUsoInternet,
    sm.Suscripciones AS SuscripcionesMoviles
FROM Paises p
LEFT JOIN PoblacionTotal pt ON pt.PaisID = p.id
LEFT JOIN UsoInternet ui ON ui.PaisID = p.id AND pt.Anio = ui.Anio
LEFT JOIN SuscripcionesMoviles sm ON sm.PaisID = p.id AND pt.Anio = sm.Anio
WHERE pt.Anio >= 2000
ORDER BY pt.Anio, p.Nombre;
```

En caso de querer filtrar por un país en específico se puede utilizar (Solo cambiar "CHL" por el código del país referenciado):

```
SELECT 
    p.Nombre AS Pais,
    p.Codigo AS CodigoPais,
    pt.Anio AS Anio,
    pt.Valor AS PoblacionTotal,
    ui.Porcentaje AS PorcentajeUsoInternet,
    sm.Suscripciones AS SuscripcionesMoviles
FROM Paises p
LEFT JOIN PoblacionTotal pt ON pt.PaisID = p.id
LEFT JOIN UsoInternet ui ON ui.PaisID = p.id AND pt.Anio = ui.Anio
LEFT JOIN SuscripcionesMoviles sm ON sm.PaisID = p.id AND pt.Anio = sm.Anio
WHERE p.Codigo = 'CHL' AND pt.Anio >= 2000
ORDER BY pt.Anio;
```

Sí se desea consultar por un año en específico:

```
SELECT 
    p.Nombre AS Pais,
    p.Codigo AS CodigoPais,
    pt.Anio AS Anio,
    pt.Valor AS PoblacionTotal,
    ui.Porcentaje AS PorcentajeUsoInternet,
    sm.Suscripciones AS SuscripcionesMoviles
FROM Paises p
LEFT JOIN PoblacionTotal pt ON pt.PaisID = p.id
LEFT JOIN UsoInternet ui ON ui.PaisID = p.id AND pt.Anio = ui.Anio
LEFT JOIN SuscripcionesMoviles sm ON sm.PaisID = p.id AND pt.Anio = sm.Anio
WHERE pt.Anio = 2010
ORDER BY p.Nombre;
```

Si se quiere consultar un dato específico filtrando por un país y por año específico:

```
SELECT 
    p.Nombre AS Pais,
    p.Codigo AS CodigoPais,
    pt.Anio AS Anio,
    pt.Valor AS PoblacionTotal,
    ui.Porcentaje AS PorcentajeUsoInternet,
    sm.Suscripciones AS SuscripcionesMoviles
FROM Paises p
LEFT JOIN PoblacionTotal pt ON pt.PaisID = p.id
LEFT JOIN UsoInternet ui ON ui.PaisID = p.id AND pt.Anio = ui.Anio
LEFT JOIN SuscripcionesMoviles sm ON sm.PaisID = p.id AND pt.Anio = sm.Anio
WHERE p.Codigo = 'CHL' AND pt.Anio = 2010
ORDER BY pt.Anio;
```


### Query para ver por País el Crecimiento vs año anterior de % personas que usan internet, suscripciones a telefonía celular móvil y población total desde 2010 en adelante (No pueden faltar países).

```
SELECT 
    p.Nombre AS Pais,
    p.Codigo AS CodigoPais,
    actual.Anio AS Anio,
    ROUND(((actual.Valor - anterior.Valor) / anterior.Valor) * 100, 2) AS CrecimientoPoblacionTotal,
    ROUND(((ui_actual.Porcentaje - ui_anterior.Porcentaje) / ui_anterior.Porcentaje) * 100, 2) AS CrecimientoUsoInternet,
    ROUND(((sm_actual.Suscripciones - sm_anterior.Suscripciones) / sm_anterior.Suscripciones) * 100, 2) AS CrecimientoSuscripcionesMoviles
FROM Paises p
LEFT JOIN PoblacionTotal actual ON actual.PaisID = p.id
LEFT JOIN PoblacionTotal anterior ON anterior.PaisID = p.id AND actual.Anio = anterior.Anio + 1
LEFT JOIN UsoInternet ui_actual ON ui_actual.PaisID = p.id AND ui_actual.Anio = actual.Anio
LEFT JOIN UsoInternet ui_anterior ON ui_anterior.PaisID = p.id AND ui_actual.Anio = ui_anterior.Anio + 1
LEFT JOIN SuscripcionesMoviles sm_actual ON sm_actual.PaisID = p.id AND sm_actual.Anio = actual.Anio
LEFT JOIN SuscripcionesMoviles sm_anterior ON sm_anterior.PaisID = p.id AND sm_actual.Anio = sm_anterior.Anio + 1
WHERE actual.Anio >= 2010
ORDER BY p.Nombre, actual.Anio;
```

Si se desea filtrar por un país específico:

```
SELECT 
    p.Nombre AS Pais,
    p.Codigo AS CodigoPais,
    actual.Anio AS Anio,
    ROUND(((actual.Valor - anterior.Valor) / anterior.Valor) * 100, 2) AS CrecimientoPoblacionTotal,
    ROUND(((ui_actual.Porcentaje - ui_anterior.Porcentaje) / ui_anterior.Porcentaje) * 100, 2) AS CrecimientoUsoInternet,
    ROUND(((sm_actual.Suscripciones - sm_anterior.Suscripciones) / sm_anterior.Suscripciones) * 100, 2) AS CrecimientoSuscripcionesMoviles
FROM Paises p
LEFT JOIN PoblacionTotal actual ON actual.PaisID = p.id
LEFT JOIN PoblacionTotal anterior ON anterior.PaisID = p.id AND actual.Anio = anterior.Anio + 1
LEFT JOIN UsoInternet ui_actual ON ui_actual.PaisID = p.id AND ui_actual.Anio = actual.Anio
LEFT JOIN UsoInternet ui_anterior ON ui_anterior.PaisID = p.id AND ui_actual.Anio = ui_anterior.Anio + 1
LEFT JOIN SuscripcionesMoviles sm_actual ON sm_actual.PaisID = p.id AND sm_actual.Anio = actual.Anio
LEFT JOIN SuscripcionesMoviles sm_anterior ON sm_anterior.PaisID = p.id AND sm_actual.Anio = sm_anterior.Anio + 1
WHERE actual.Anio >= 2010
  AND p.Codigo = 'CHL'
ORDER BY actual.Anio;
```


## Uso de Scripts

Usar solo en caso de no poder exportar la base de datos o ver el funcionamiento de los scripts.

### conversor.py
En caso de tener solo los excel en formato xls, se debe correr este para convertir a formato xlsx y poder trabajar con estos con la librería de pandas.

### poblar_bd.py
Este script se encarga de llenar con los datos entragados la base de datos, tomando ciertas consideraciones para el análisis efectivo de las métricas.

- En caso de no encontrarse el nombre de un país este llena con 'Desconocido'.
- En caso de no tener el primer valor, este se completa con 0.
- En caso de faltar un valor intermedio o final, este se completa con el valor del año anterior.