import requests
import time

class HEK:

    """

    Attributes:

    Args:
        event_starttime:
        event_endtime
    """

    def __init__(self, event_starttime, event_endtime):
        self._event_starttime = event_starttime
        self._event_endtime = event_endtime


    def __nearest_point(self, _list, number):
        """
        Takes the nearest number inside a list, of a given number.
        """
        return min(_list, key=lambda n: abs(n - (number)))


    def __get_url(self, event_type):
        if event_type != "fl" and event_type != "ar":
            print("Invalid event type")
            return False

        url = "http://www.lmsal.com/hek/her?"
        url += "cmd=search&type=column&event_type={}".format(event_type)
        url += "&event_starttime={}".format(self._event_starttime)
        url += "&event_endtime={}".format(self._event_endtime)
        url += "&event_coordsys=helioprojective"
        url += "&x1=-1200&x2=1200&y1=-1200&y2=1200"
        url += "&cosec=2"
        return url


    def __get_rhessi_points(self):
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


    def __compare_rhessi_points(self):
        ar_url = self.__get_url("ar")
        ar_req = requests.get(ar_url)
        self.ar_data = ar_req.json()

        x_points = []
        y_points = []

        for ar_result in self.ar_data['result']:
            x_points.append(ar_result['hgc_x'])
            y_points.append(ar_result['hgc_y'])

        # Pegas os pontos mais próximos, analisando todos os pontos dentro da lista,
        # e comparando com os dados pegos do rhessi.
        self._y_point = self.__nearest_point(y_points, self._y_rhessi)
        self._x_point = self.__nearest_point(x_points, self._x_rhessi)


    def get_active_region(self):
        self.__get_rhessi_points()
        self.__compare_rhessi_points()

        rhessi_x_diference = abs(self._x_point - self._x_rhessi)
        rhessi_y_diference = abs(self._y_point - self._y_rhessi)

        if rhessi_x_diference < rhessi_y_diference:
            for ar_result in self.ar_data['result']:
                if ar_result['hgc_x'] == self._x_point:
                    self.active_region = ar_result['hgs_coord']
        else:
            for ar_result in self.ar_data['result']:
                if ar_result['hgc_y'] == self._y_point:
                    self.active_region = ar_result['hgs_coord']

        return self.active_region
