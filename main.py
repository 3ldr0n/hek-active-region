import requests
import time

def ponto_mais_proximo(lista, numero):
    """
    Essa funcao pega o número mais próximo, de um certo número dentro
    de uma lista.
    """
    return min(lista, key=lambda n: abs(n - (numero)))

event_starttime = '2002-04-09T12:45:00'
event_endtime = '2002-04-09T13:05:00'
event_type = 'fl'

def get_url(event_starttime, event_endtime, event_type):
    url = "http://www.lmsal.com/hek/her?"
    url += "cmd=search&type=column&event_type={}".format(event_type)
    url += "&event_starttime={}".format(event_starttime)
    url += "&event_endtime={}".format(event_endtime)
    url += "&event_coordsys=helioprojective&x1=-1200&x2=1200&y1=-1200&y2=1200"
    url += "&cosec=2"
    return url

fl_url = get_url(event_starttime, event_endtime, event_type)
fl_req = requests.get(fl_url)
fl_data = fl_req.json()

for piece_of_data in fl_data['result']:
    if piece_of_data['search_instrument'] == "RHESSI":
        posicao_rhessi = 'RHESSI ', piece_of_data['hgc_coord']

        ponto_x_rhessi = float(posicao_rhessi[1][6:16])
        ponto_y_rhessi = float(posicao_rhessi[1][17:24])

ar_url = get_url(event_starttime, event_endtime, 'ar')
ar_req = requests.get(ar_url)
ar_data = ar_req.json()

ponto_x = []
ponto_y = []

for data in ar_data['result']:
    ponto_x.append(data['hgc_x'])
    ponto_y.append(data['hgc_y'])

# Pegas os pontos mais próximos, analisando todos os pontos dentro da lista,
# e comparando com os dados pegos do rhessi.
ponto_y = [ponto_mais_proximo(ponto_y, ponto_y_rhessi)]
ponto_x = [ponto_mais_proximo(ponto_x, ponto_x_rhessi)]

ponto_y = ponto_y[0]
ponto_x = ponto_x[0]

print(ponto_x)
print(ponto_y)

for data in ar_data['result']:
    print(data['hgs_coord'])

for i in ar_data['result']:
    print(i['hgs_coord'])
