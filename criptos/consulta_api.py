import requests
from criptos import app


API_KEY = app.config['API_KEY']

def api(form):
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'
    resultado = requests.get(url.format(form.c1.data, form.desde_moneda.data, form.para_moneda.data, API_KEY))
    if resultado.status_code == 200:
        datos = resultado.json()
        return datos
    else:
        error = ("Error en API_KEY. Vuelva a intentarlo")
        return error