import requests
import time

class HEK:

    """
    event_starttime = '2002-04-09T12:45:00'
    event_endtime = '2002-04-09T13:05:00'

    hek = HEK(event_starttime, event_endtime)
    hek.get_rhessi_points()
    ar = hek.get_active_region()
    print("\n{}\n".format(ar))
    """

    def __init__(self, event_starttime, event_endtime):
        self._event_starttime = event_starttime
        self._event_endtime = event_endtime


    def __nearest_point(self, lista, numero):
        """
        Essa funcao pega o número mais próximo, de um certo número dentro
        de uma lista.
        """
        return min(lista, key=lambda n: abs(n - (numero)))


    def __get_url(self, event_type):
        url = "http://www.lmsal.com/hek/her?"
        url += "cmd=search&type=column&event_type={}".format(event_type)
        url += "&event_starttime={}".format(self._event_starttime)
        url += "&event_endtime={}".format(self._event_endtime)
        url += "&event_coordsys=helioprojective"
        url += "&x1=-1200&x2=1200&y1=-1200&y2=1200"
        url += "&cosec=2"
        return url


    def get_rhessi_points(self):
        fl_url = self.__get_url("fl")
        fl_req = requests.get(fl_url)
        fl_data = fl_req.json()

        for fl_result in fl_data['result']:
            if fl_result['search_instrument'] == "RHESSI":
                rhessi_position = 'RHESSI ', fl_result['hgc_coord']
                rhessi_coord = fl_result['hgs_coord']

                self._x_rhessi = float(rhessi_position[1][6:16])
                self._y_rhessi = float(rhessi_position[1][17:24])

        return self._x_rhessi, self._y_rhessi


    def _compare_rhessi_points(self):
        ar_url = self.__get_url("ar")
        ar_req = requests.get(ar_url)
        self.ar_data = ar_req.json()

        ponto_x = []
        ponto_y = []

        for ar_result in self.ar_data['result']:
            ponto_x.append(ar_result['hgc_x'])
            ponto_y.append(ar_result['hgc_y'])

        # Pegas os pontos mais próximos, analisando todos os pontos dentro da lista,
        # e comparando com os dados pegos do rhessi.
        self._ponto_y = self.__nearest_point(ponto_y, self._y_rhessi)
        self._ponto_x = self.__nearest_point(ponto_x, self._x_rhessi)


        print("Ponto x: {}\nPonto y: {}".format(self._ponto_x, self._ponto_y))
        print("Ponto x RHESSI: {}\nPonto y RHESSI: {}"
                                .format(self._x_rhessi, self._y_rhessi))


    def get_active_region(self):
        self._compare_rhessi_points()

        diferenca_x_rhessi = abs(self._ponto_x - self._x_rhessi)
        diferenca_y_rhessi = abs(self._ponto_y - self._y_rhessi)

        print("Diferença x: ", diferenca_x_rhessi)
        print("Diferença y: ", diferenca_y_rhessi)

        if diferenca_x_rhessi < diferenca_y_rhessi:
            for ar_result in self.ar_data['result']:
                if ar_result['hgc_x'] == self._ponto_x:
                    self.active_region = ar_result['hgs_coord']
        else:
            for ar_result in self.ar_data['result']:
                if ar_result['hgc_y'] == self._ponto_y:
                    self.active_region = ar_result['hgs_coord']

        print("Região Ativa: {}".format(self.active_region))
        return self.active_region
