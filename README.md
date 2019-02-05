# Nazk
[![PyPI version](https://badge.fury.io/py/nazk.svg)](https://pypi.org/project/nazk/)

## Descripción
Obtén el tipo de cambio oficial de la SBS y SUNAT (Perú) en tiempo real. Nazk es una librería escrita en Python 3.6 que permite obtener de manera rápida y sencilla el tipo de cambio por día o rango de días.

## Instalación
```
pip install nazk
```

## Uso básico
```python
from nazk import Nazk

nk = Nazk()
data = nk.get_exchange_rate('USD', '01/01/2019', '10/01/2019')
print(data)
```
Obtendremos el siguiente resultado:
```python
{'01/01/2019': {'buy': '3.369', 'sell': '3.379'}, '02/01/2019': {'buy': '3.369', 'sell': '3.373'}, '03/01/2019': {'buy': '3.368', 'sell': '3.371'}, '04/01/2019': {'buy': '3.356', 'sell': '3.360'}, '05/01/2019': {'buy': '3.356', 'sell': '3.360'}, '06/01/2019': {'buy': '3.356', 'sell': '3.360'}, '07/01/2019': {'buy': '3.349', 'sell': '3.353'}, '08/01/2019': {'buy': '3.347', 'sell': '3.350'}, '09/01/2019': {'buy': '3.333', 'sell': '3.335'}, '10/01/2019': {'buy': '3.341', 'sell': '3.343'}}
```

## Configuración
| Opción        | Descripción                                | Predeterminado | Valores permitidos |
|:-------------:|--------------------------------------------|:--------------:|:------------------:|
| `source`      | La fuente de dónde se obtendrán los datos. | `SBS`          | `SBS`, `SUNAT`.    |
| `date_format` | Formato de fecha devuelto.                 | `%d/%m/%Y`     | [http://strftime.org](http://strftime.org) |

## Ejemplo SUNAT
```python
from nazk import Nazk

nk = Nazk(source='SUNAT', date_format='%d-%m-%y')
data = nk.get_exchange_rate('USD', '01/01/2019', '10/01/2019')
print(data)
```
Obtendremos el siguiente resultado:
```python
{'01-01-19': {'buy': '3.369', 'sell': '3.379'}, '02-01-19': {'buy': '3.369', 'sell': '3.379'}, '03-01-19': {'buy': '3.369', 'sell': '3.373'}, '04-01-19': {'buy': '3.368', 'sell': '3.371'}, '05-01-19': {'buy': '3.356', 'sell': '3.360'}, '06-01-19': {'buy': '3.356', 'sell': '3.360'}, '07-01-19': {'buy': '3.356', 'sell': '3.360'}, '08-01-19': {'buy': '3.349', 'sell': '3.353'}, '09-01-19': {'buy': '3.347', 'sell': '3.350'}, '10-01-19': {'buy': '3.333', 'sell': '3.335'}}
```

## Divisas
Listado de divisas permitidas.

| Divisa               |  ISO  |
|----------------------|:-----:|
| Dólar estadounidense | `USD` |
| Corona Sueca         | `SEK` |
| Franco Suizo         | `CHF` |
| Dólar canadiense     | `CAD` |
| Euro                 | `EUR` |
| Yen japonés          | `JPY` |
| Libra esterlina      | `GBP` |

## Métodos
#### get_exchange_rate(`currency, from_date, to_date=None`)
Obtener el tipo de cambio de la moneda indicada por fecha o rango de fechas. Devolverá por defecto un diccionario ([https://docs.python.org/3.6/tutorial/datastructures.html#dictionaries](https://docs.python.org/3.6/tutorial/datastructures.html#dictionaries)).

## Consideraciones
* Sólo se puede obtener el tipo de cambio desde el año 2000 en adelante.
* El tipo de cambio de la SUNAT es el tipo de cambio del cierre del día anterior de la SBS (fuente [http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias](http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias)).
* El tipo de cambio no se publica en la SBS o SUNAT todos los díás. En estos casos se tomará el tipo de cambio del día anterior.

