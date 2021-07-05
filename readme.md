# :chart_with_downwards_trend:  Cripto-Conversor  :chart_with_upwards_trend:

### Proyecto desarrollado con Flask | Bootcamp Zero de KeepCoding  :computer:
___
Aplicación que simula la compraventa de las siguintes 12 criptomonedas: 


1.Bitcoin 'BTC'

2.Ethereum 'ETH'

3.Teher 'USDT'

4.Binance 'BNB'

5.Cardano 'ADA'

6.XRP 'XRP'

7.Bitcoin Cash 'BCH'

8.Stellar 'XLM'

9.Tron 'TRX'

10.EOS 'EOS'

11.Bitcoin SV 'BSV'

12.Litecoin 'LTC'

Se dispondrá de un saldo infinito en **euros €** para comprar. Las criptomonedas pueden intercambiarse entre ellas con el objetivo de hacer crecer nuestras inversiones. Para recuperar las inversiones de cualquier cripto, deberán intercambiarse por **euros €**.

Instalación :mag_right:
___
* **Creación del entorno virtual en Windows (opcional)**

**python -m venv venv**

* **Creación del entorno virtual en Mac y Linux (opcional)**

**python3 -m venv venv**

* **Instalación del fichero requirements**

**pip install -r requirements.txt**


* **Fichero .env_template**

Deberá duplicarse este fichero y renombrarlo a **.env**. Será elección del instalador si quiere trabajar en modo development o production.

* **Fichero config_template.py**

Deberá duplicarse este fichero y renombrarlo a **config.py** en él tendrás que realizar estos 3 pasos:

1. Deberás establecer una clave secreta. Un buen sitio para encontrarla es randomkeygen.com
2. Necesitarás una clave para la API. Visita coinmarketcap.com/api/ para obtenerla
3. Establecer la ruta a tu base de datos.


* **Creación de la base de datos**

Informar de la ruta a la base de datos **data/movimientos.db** y ejecutar el fichero initial.sql dentro de la carpeta migrations. Se puede realizar con sqlite3 o con un cliente gráfico.

* **Iniciar la aplicación**

Ejecutar el comando: 
> flask run


