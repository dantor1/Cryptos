from criptos import app
from flask import render_template, flash, request, redirect, url_for
from criptos.forms import MovimientosForm
from datetime import datetime
import requests
from criptos.dataaccess import *
from criptos.consulta_api import *


API_KEY = app.config['API_KEY']
url_api = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'


def validaciones_criptos():
    try:
        compra_venta = consultaSQL("SELECT * FROM movimientos;")
        monedasdict = dict()
        for i in compra_venta:
            # Cuando compremos por 1ª vez el saldo será negativo. En el else las segundas y sucesivas compras las vamos acumulando con saldo negativo.
            if i['moneda_from'] not in monedasdict:
                monedasdict[i['moneda_from']] = -i['cantidad_from']
            else: 
                monedasdict[i['moneda_from']] -= i['cantidad_from']
            # Cuando vendamos/intercambiemos si no está la añadimos. En el else vamos sumándola acumulándolas en el diccionario.
            if i['moneda_to'] not in monedasdict:
                monedasdict[i['moneda_to']] = i['cantidad_to']
            else: 
                monedasdict[i['moneda_to']] += i['cantidad_to']
        return monedasdict
    except:
        flash("Se ha producido un error en la base de datos. Pruebe en unos minutos")
        return render_template("compra.html")


@app.route('/')
def index():
    try:
        movimientos = consultaSQL("SELECT * FROM movimiento ORDER BY date;")
        return render_template("inicio.html", movimientos=movimientos)
    except:
        flash("Error en base de datos. Inténtelo de nuevo", "error")
        return render_template("inicio.html")


@app.route('/compra', methods=["GET", "POST"])
def compra():
    formulario = MovimientosForm()

    monedas_actuales = validaciones_criptos()
    listacriptos = ['ADA', 'BCH', 'BNB', 'BSV', 'BTC', 'EOS', 'ETH', 'EUR', 'LTC', 'TRX', 'USDT', 'XLM', 'XRP']
    
    mismonedas = list(monedas_actuales.keys())
    # Inicializamos siempre con EUR, porque siempre tendremos disponible de esta moneda. monedas_actuales llamará a la función validaciones_criptos para saber cuantas monedas hay en cada momento.
    mismonedas.append('EUR')


    formulario.desde_moneda.choices = mismonedas
    formulario.para_moneda.choices = listacriptos    
    if request.method == "POST":
        if 'submit2' in request.form:
            if type(formulario.c1.data) is not float:
                flash("No se permiten cadenas de texto")
                return render_template('compra.html', form=formulario)     
            if formulario.c1.data > 1000000000:
                flash("El importe máximo tiene que estar por debajo de 1.000.000.000 ")
                return render_template('compra.html', form=formulario)     
            if formulario.desde_moneda.data == formulario.para_moneda.data:
                flash("Las monedas From y To tienen que ser distintas")
                return render_template('compra.html', form=formulario)     
            resultado = api(formulario)
            if not isinstance(resultado, str):
                precio = resultado['data']['quote'][formulario.para_moneda.data]['price']
                precioprocesado = precio 
                formulario.c2.data = precioprocesado
                punitario = formulario.c1.data/precio 
                formulario.c2.data = precioprocesado
                return render_template("compra.html", form=formulario, cantidadconvertida=precioprocesado, preciounitario=punitario)
            else:
                error=("Error")
                flash(error)
                return render_template('compra.html', form=formulario)
    
        # Si el formulario llega con los datos, se debe verificar que se cumplen todos los requisitos(formato, monedas distintas, etc)
        if formulario.validate():
            saldo_actualizado = validaciones_criptos()
            if formulario.desde_moneda.data != 'EUR':
                saldo=float((saldo_actualizado[formulario.desde_moneda.data]))
            if formulario.desde_moneda.data !='EUR' and formulario.c1.data > saldo:
                flash('Saldo insuficiente para realizar la compra')
                return render_template("compra.html", form=formulario)
            if formulario.desde_moneda.data == formulario.para_moneda.data:
                flash("Las monedas From y To tienen que ser distintas")
                return render_template("compra.html", form=formulario)
            if formulario.c1.data > 1000000000:
                flash("El importe máximo tiene que estar por debajo de 1.000.000.000 ")
                return render_template("compra.html", form=formulario)

            # Con try-except capturamos el error en caso de que no se realice la compra y se grabe en la BBDD correctamente
            formulario.preciounitario.data = formulario.c1.data/formulario.c2.data
            try:
                consultaSQL("INSERT INTO movimientos (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, preciounitario) VALUES (?, ?, ?, ?, ?, ?, ?);", (str(datetime.now().strftime('%Y-%m-%d')), str(datetime.now().strftime('%H:%M:%S.%f')[:-3]), formulario.desde_moneda.data, "{0:.2f}".format(formulario.c1.data), formulario.para_moneda.data, "{0:.8f}".format(formulario.c2.data), "{0:.8f}".format(formulario.preciounitario.data))) 
            except sqlite3.Error as el_error:
                print("Error en SQL", el_error)
                flash("Error en base de datos: no se ha realizado la compra", "error")
                return render_template('compra.html', form=formulario)
        # Si entra por aquí es porque no ha validado el formulario. No se ha hecho click en el boton de la calculadora
        else:
            flash("Antes de comprar debes calcular la compra a realizar")
            return render_template("compra.html", form=formulario)

    return render_template("compra.html", form=formulario)   


@app.route('/status')
def status():
    saldosmonedas = validaciones_criptos()
    print("saldosmonedas:", saldosmonedas)
    print("saldosmonedas:", saldosmonedas.items())

    # Consultamos en la base de datos para acceder a las monedas from que sean "EUR"    
    try:
        from_dinero = consultaSQL('SELECT cantidad_from FROM movimientos WHERE moneda_from = "EUR"')    
    except sqlite3.Error as el_error:
        print("Error en SQL", el_error)
        flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error")
        saldos = 0
        return render_template("status.html", saldos=saldos)
    # Consultamos en la base de datos para acceder a las monedas to que sean "EUR"
    try:
        to_dinero = consultaSQL('SELECT cantidad_to FROM movimientos WHERE moneda_to = "EUR"')
    except sqlite3.Error as el_error:
        print("Error en SQL", el_error)
        flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error")
        saldos = 0
        return render_template("status.html", saldos=saldos)

    # INVERSIÓN ATRAPADA: Calculamos el valor actual de todas las criptos, quitándole los 'EUR' si los hubiera
    if 'EUR' in saldosmonedas:
        del saldosmonedas['EUR']
    else:
        pass
    inv_atrapada=0
    for item, valor in saldosmonedas.items():
        resultado = requests.get(url_api.format(valor, item, 'EUR', API_KEY))
        if resultado.status_code == 200:
            dict_precios = resultado.json()
            # Procesamos los datos necesarios del diccionario de diccionarios que devuelve el json hasta llegar al valor actual de la cripto
            cotizacionactual = dict_precios['data']['quote']['EUR']['price']
            inv_atrapada+=cotizacionactual
        if resultado.status_code != 200:
            flash("Error en API_KEY")
            return render_template("status.html", saldos=0)
    
    euros_from=0
    for i in from_dinero:
        euros_from += i['cantidad_from']
    
    euros_to=0
    for i in to_dinero:
        euros_to += i['cantidad_to']
    
    saldos_euros_invertidos = euros_to - euros_from
    cantidadinvertida = round(euros_from, 2)
    precioactual = round(cantidadinvertida + saldos_euros_invertidos + inv_atrapada, 2)
    diferencia = precioactual - cantidadinvertida
    return render_template("status.html", cantidadinvertida=cantidadinvertida, precioactual=precioactual, saldos=diferencia)   

    
