from django.shortcuts import render
import requests
# Create your views here.
def inicio(request):
    return render(request, 'inicio/index.html')

def listar_personas(request):
    personas = {
        'titulo': 'Lista de personas',
        'nombres': ['alicia', 'beto', 'carlos', 'diana']
    }
    return render(request, 'inicio/listar-personas.html', personas)


def crypto_price(request):
    pagina = 1
    if request.GET:
        pagina = int(request.GET['page'])
    url_binance = 'https://api.binance.com/api/v3/ticker/price'
    datos = requests.get(url_binance)
    contexto = {'precios': datos.json()[int(pagina)*10-9:int(pagina)*10:]}
    return render(request, 'inicio/crypto_price.html', contexto)


def people_directory(request):
    url_directory = 'https://jsonplaceholder.typicode.com/users'
    datos = requests.get(url_directory)
    contexto = {'personas': datos.json()}
    return render(request, 'inicio/people_directory.html', contexto)


