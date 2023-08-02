from decimal import Decimal
from math import sqrt
from math import ceil
from itertools import combinations


class Punkt:
    def __init__(self, x, y, wyspa):
        self.x = x
        self.y = y
        self.wyspa = wyspa
        self.index = 0
        self.odcinki = []

    def __eq__(self, punkt):
        return self.x == punkt.x and self.y == punkt.y and self.wyspa.nazwa == punkt.wyspa.nazwa


class Wierzcholek(Punkt):
    def __init__(self, x, y, strefa, wyspa):
        super().__init__(x, y, wyspa)
        self.strefa = strefa

    def drukuj(self):
        return str(int(self.x)) + " " + str(int(self.y))


class Baza(Punkt):
    def __init__(self, x, y, nazwa, wyspa):
        super().__init__(x, y, wyspa)
        self.nazwa = nazwa.strip()
        self.index_globalny = None
        self.polaczenia_wewnetrzne = []
        self.polaczenia_zewnetrzne = []
        self.lista_polaczen_posrednich = []

    def drukuj(self):
        return self.nazwa + " " + self.wyspa.nazwa


class Strefa:
    def __init__(self, x1, y1, x2, y2, wyspa):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.wyspa = wyspa
        self.punkt_a = Wierzcholek(x1, y1, self, self.wyspa)
        self.punkt_b = Wierzcholek(x2, y2, self, self.wyspa)
        self.punkt_c = Wierzcholek(x1, y2, self, self.wyspa)
        self.punkt_d = Wierzcholek(x2, y1, self, self.wyspa)

    def zwroc_punkty(self):
        return [self.punkt_a, self.punkt_b, self.punkt_c, self.punkt_d]

    def drukuj(self, tekst="Drukuje strefe = "):
        print(tekst, self.x1, self.y1, self.x2, self.y2)


class Polaczenie:
    def __init__(self, punkt_poczatkowy, punkt_docelowy):
        self.punkt_poczatkowy = punkt_poczatkowy
        self.punkt_docelowy = punkt_docelowy


class Trasa(Polaczenie):
    def __init__(self, punkt_poczatkowy, punkt_docelowy, poprzedzajaca_trasa=None, odcinek=None, dystans=1000000):
        super().__init__(punkt_poczatkowy, punkt_docelowy)
        self.najkrotsza_trasa_do_punktu_docelowego = poprzedzajaca_trasa
        self.odcinek = odcinek
        self.dystans = dystans

    def wyswietl_trase(self):
        if not (self.punkt_poczatkowy == self.punkt_docelowy):
            if self.najkrotsza_trasa_do_punktu_docelowego is not None:
                self.najkrotsza_trasa_do_punktu_docelowego.wyswietl_trase()
                print(self.punkt_docelowy.drukuj())

    def porownaj_trasy_zwroc_optymalniejsza(self, trasa_druga):
        if self.punkt_poczatkowy == trasa_druga.punkt_poczatkowy and self.punkt_docelowy == trasa_druga.punkt_docelowy:
            if self.dystans > trasa_druga.dystans:
                return trasa_druga
            elif self.dystans < trasa_druga.dystans:
                return self

            elif self.dystans == trasa_druga.dystans:
                if self.najkrotsza_trasa_do_punktu_docelowego == trasa_druga.najkrotsza_trasa_do_punktu_docelowego:
                    return self
                else:
                    licznik_1 = 0
                    sprawdzam = False
                    temp_punkt_1 = self.najkrotsza_trasa_do_punktu_docelowego
                    temp_punkt_2 = trasa_druga.najkrotsza_trasa_do_punktu_docelowego
                    while not sprawdzam:
                        if temp_punkt_1.najkrotsza_trasa_do_punktu_docelowego is None:
                            sprawdzam = True
                        else:
                            temp_punkt_1 = temp_punkt_1.najkrotsza_trasa_do_punktu_docelowego
                            licznik_1 += 1
                    licznik_2 = 0
                    sprawdzam = False
                    while not sprawdzam:
                        if temp_punkt_2.najkrotsza_trasa_do_punktu_docelowego is None:
                            sprawdzam = True
                        else:
                            temp_punkt_2 = temp_punkt_2.najkrotsza_trasa_do_punktu_docelowego
                            licznik_2 += 1
                    if licznik_1 < licznik_2:
                        return self
                    elif licznik_1 > licznik_2:
                        return trasa_druga
                    elif licznik_1 == licznik_2:
                        return trasa_druga
        else:
            raise "nie powinno sie wydarzyc"


class PolaczenieMiedzywyspowe(Polaczenie):
    def __init__(self, punkt_poczatkowy, wyspa_1, punkt_docelowy, wyspa_2, dystans):
        super().__init__(punkt_poczatkowy, punkt_docelowy)
        self.dystans = dystans
        self.punkt_poczatkowy = punkt_poczatkowy
        self.punkt_docelowy = punkt_docelowy
        self.wyspa_1 = wyspa_1
        self.wyspa_2 = wyspa_2

    @staticmethod
    def wczytaj_dane_polaczenia(wyspy, dane_wejsciowe):
        baza_1, wyspa_1, baza_2, wyspa_2, dystans = dane_wejsciowe.split()
        baza_1_zidentyfikowana = None
        wyspa_1_zidentyfikowana = None
        baza_2_zidentyfikowana = None
        wyspa_2_zidentyfikowana = None
        for wyspa in wyspy:
            if wyspa.nazwa.strip() == wyspa_1:
                wyspa_1_zidentyfikowana = wyspa
                for baza in wyspa.bazy:
                    if baza.nazwa.strip() == baza_1:
                        baza_1_zidentyfikowana = baza
                        break
            elif wyspa.nazwa.strip() == wyspa_2:
                wyspa_2_zidentyfikowana = wyspa
                for baza in wyspa.bazy:
                    if baza.nazwa.strip() == baza_2:
                        baza_2_zidentyfikowana = baza
                        break
        baza_1_zidentyfikowana.polaczenia_zewnetrzne.append(
            PolaczenieMiedzywyspowe(baza_1_zidentyfikowana, wyspa_1_zidentyfikowana, baza_2_zidentyfikowana,
                                    wyspa_2_zidentyfikowana, Decimal(dystans)))
        baza_2_zidentyfikowana.polaczenia_zewnetrzne.append(
            PolaczenieMiedzywyspowe(baza_2_zidentyfikowana, wyspa_2_zidentyfikowana, baza_1_zidentyfikowana,
                                    wyspa_1_zidentyfikowana, Decimal(dystans)))


class TrasaGlobalna(Trasa):
    def __init__(self, punkt_poczatkowy, punkt_docelowy, poprzedzajaca_trasa=None, odcinek=None, dystans=1000000):
        super().__init__(punkt_poczatkowy, punkt_docelowy, poprzedzajaca_trasa, odcinek, dystans)

    def wyswietl_trase(self):
        if not (self.punkt_poczatkowy == self.punkt_docelowy):
            if self.najkrotsza_trasa_do_punktu_docelowego is not None:
                self.najkrotsza_trasa_do_punktu_docelowego.wyswietl_trase()
                if type(self.odcinek) is Trasa:
                    self.odcinek.wyswietl_trase()
                elif type(self.odcinek) is PolaczenieMiedzywyspowe:
                    print(self.punkt_docelowy.drukuj())

    def porownaj_trasy_zwroc_optymalniejsza(self, trasa_druga):
        if self.punkt_poczatkowy == trasa_druga.punkt_poczatkowy and self.punkt_docelowy == trasa_druga.punkt_docelowy:
            if self.dystans > trasa_druga.dystans:
                return trasa_druga
            elif self.dystans < trasa_druga.dystans:
                return self
            else:
                return self
        else:
            raise "nie powinno sie wydarzyc"


class Odcinek:
    def __init__(self, punkt_a, punkt_b, licz_dlugosc=False):
        self.punkt_a = punkt_a
        self.punkt_b = punkt_b
        if (punkt_a.x - punkt_b.x != 0) and (punkt_a.y - punkt_b.y != 0):
            self.a = (punkt_a.y - punkt_b.y) / (punkt_a.x - punkt_b.x)
            self.b = punkt_a.y - self.a * punkt_a.x
            self.charakter = "skosny"
        elif punkt_a.x == punkt_b.x:
            self.a = punkt_a.x
            self.b = punkt_a.x
            self.charakter = "pionowy"
        elif punkt_a.y == punkt_b.y:
            self.a = punkt_b.y
            self.b = punkt_b.y
            self.charakter = "poziomy"
        if licz_dlugosc:
            self.dystans = sqrt(abs(self.punkt_a.x - self.punkt_b.x) ** 2 + abs(self.punkt_a.y - self.punkt_b.y) ** 2)
        else:
            self.dystans = 0

    def dlugosc(self):
        if self.dystans == 0:
            return sqrt(abs(self.punkt_a.x - self.punkt_b.x) ** 2 + abs(self.punkt_a.y - self.punkt_b.y) ** 2)
        else:
            return self.dystans

    def drukuj(self, komentarz=""):
        print(str(self.punkt_a.drukuj()) + " " + str(self.punkt_b.drukuj()) + " dlugosc = " + str(round(self.dlugosc(), 4)) + " " + komentarz)

    def czy_odcinek_przecina_jakies_strefy(self, strefy):
        # Funkcja czy_odcinek_przecina_jakies_strefy na podstawie rowniania prostej(odcinka) stworzonego dzieki rownaniu
        # y=ax+b i punktom oblicza, czy pojawia sie taki punkt w ktorym rownanie y=ax+b zachodzi, z zastrzezeniem
        # ograniczonego obszaru odcinka, nie zas przez caly uklad wspolrzednych.
        # Dodatkowo obsluguje sytuacje kiedy odcinek jest rownolegly do osi x albo osi y.
        # Jeszcze dodatkowo, obslugujemy sytuacje kiedy odcinek staje sie przekontna strefy wykluczenia. Jest to
        # konieczne poniewaz podobna sytacja wystepuje kiedy odcinek(trasa) przechodzi, przez któryś z bokow. Tez dwa
        # wierzcholki sa przeciete ale wtedy nie jest naruszamy strefy.
        # self.drukuj()
        if not type(strefy) is list:
            strefy = [strefy]

        for strefa in strefy:
            if self.charakter == "skosny":
                # sprzawdzamy czy odcinek jest w zasiegu strefy
                # strefa.drukuj()
                # strefax1_w_zasiegu_odcinka = min(self.punkt_a.x, self.punkt_b.x) < strefa.x1 < max(self.punkt_a.x, self.punkt_b.x)
                # strefax2_w_zasiegu_odcinka = min(self.punkt_a.x, self.punkt_b.x) < strefa.x2 < max(self.punkt_a.x, self.punkt_b.x)
                # strefay1_w_zasiegu_odcinka = min(self.punkt_a.y, self.punkt_b.y) < strefa.y1 < max(self.punkt_a.y, self.punkt_b.y)
                # strefay2_w_zasiegu_odcinka = min(self.punkt_a.y, self.punkt_b.y) < strefa.y2 < max(self.punkt_a.y, self.punkt_b.y)
                # temp1_y_w_zaisegu = min(strefa.y1, strefa.y2) < Decimal(self.a * strefa.x1 + self.b) < max(strefa.y1, strefa.y2)
                # temp2_y_w_zaisegu = min(strefa.y1, strefa.y2) < Decimal(self.a * strefa.x2 + self.b) < max(strefa.y1, strefa.y2)
                # temp1_x_w_zaisegu = min(strefa.x1, strefa.x2) < Decimal((strefa.y1 - self.b) / self.a) < max(strefa.x1, strefa.x2)
                # temp2_x_w_zaisegu = min(strefa.x1, strefa.x2) < Decimal((strefa.y2 - self.b) / self.a) < max(strefa.x1, strefa.x2)

                # if strefax1_w_zasiegu_odcinka and temp1_y_w_zaisegu:
                if ((min(self.punkt_a.x, self.punkt_b.x) < strefa.x1 < max(self.punkt_a.x, self.punkt_b.x)) and
                        (min(strefa.y1, strefa.y2) < Decimal(self.a * strefa.x1 + self.b) < max(strefa.y1, strefa.y2))):
                    return True
                # elif strefax2_w_zasiegu_odcinka and temp2_y_w_zaisegu:
                elif ((min(self.punkt_a.x, self.punkt_b.x) < strefa.x2 < max(self.punkt_a.x, self.punkt_b.x)) and
                      (min(strefa.y1, strefa.y2) < Decimal(self.a * strefa.x2 + self.b) < max(strefa.y1, strefa.y2))):
                    return True
                # elif temp1_x_w_zaisegu and strefay1_w_zasiegu_odcinka:
                elif ((min(self.punkt_a.y, self.punkt_b.y) < strefa.y1 < max(self.punkt_a.y, self.punkt_b.y)) and
                      (min(strefa.x1, strefa.x2) < Decimal((strefa.y1 - self.b) / self.a) < max(strefa.x1, strefa.x2))):
                    return True
                # elif strefay2_w_zasiegu_odcinka and temp2_x_w_zaisegu:
                elif ((min(self.punkt_a.y, self.punkt_b.y) < strefa.y2 < max(self.punkt_a.y, self.punkt_b.y)) and
                      (min(strefa.x1, strefa.x2) < Decimal((strefa.y2 - self.b) / self.a) < max(strefa.x1, strefa.x2))):
                    return True

                # tu jest fragment obslugujacy sytuacje gdy odcinek jest przekatna
                elif (((Wierzcholek(Decimal((strefa.y1 - self.b) / self.a), Decimal(self.a * strefa.x1 + self.b), strefa, strefa.wyspa) == strefa.punkt_a and
                        Wierzcholek(Decimal((strefa.y2 - self.b) / self.a), Decimal(self.a * strefa.x2 + self.b), strefa, strefa.wyspa) == strefa.punkt_b) or
                       (Wierzcholek(Decimal((strefa.y2 - self.b) / self.a), Decimal(self.a * strefa.x2 + self.b), strefa, strefa.wyspa) == strefa.punkt_a and
                        Wierzcholek(Decimal((strefa.y1 - self.b) / self.a), Decimal(self.a * strefa.x1 + self.b), strefa, strefa.wyspa) == strefa.punkt_b)) and
                      ((self.punkt_a.x <= strefa.x1 and self.punkt_b.x >= strefa.x2) or
                       (self.punkt_a.x >= strefa.x1 and self.punkt_b.x <= strefa.x2))):
                    return True
                elif (((Wierzcholek(Decimal((strefa.y2 - self.b) / self.a), Decimal(self.a * strefa.x1 + self.b), strefa, strefa.wyspa) == strefa.punkt_c and
                        Wierzcholek(Decimal((strefa.y1 - self.b) / self.a), Decimal(self.a * strefa.x2 + self.b), strefa, strefa.wyspa) == strefa.punkt_d) or
                       (Wierzcholek(Decimal((strefa.y1 - self.b) / self.a), Decimal(self.a * strefa.x2 + self.b), strefa, strefa.wyspa) == strefa.punkt_c and
                        Wierzcholek(Decimal((strefa.y2 - self.b) / self.a), Decimal(self.a * strefa.x1 + self.b), strefa, strefa.wyspa) == strefa.punkt_d)) and
                      ((self.punkt_a.x <= strefa.x1 and self.punkt_b.x >= strefa.x2) or
                       (self.punkt_a.x >= strefa.x1 and self.punkt_b.x <= strefa.x2))):
                    return True

            elif self.charakter == "pionowy":
                if (min(strefa.x1, strefa.x2) < self.a < max(strefa.x1, strefa.x2) and
                        min(self.punkt_a.y, self.punkt_b.y) < strefa.y1 < max(self.punkt_a.y, self.punkt_b.y)):
                    return True
            elif self.charakter == "poziomy":
                if (min(strefa.y1, strefa.y2) < self.a < max(strefa.y1, strefa.y2) and
                        min(self.punkt_a.x, self.punkt_b.x) < strefa.x1 < max(self.punkt_a.x, self.punkt_b.x)):
                    return True
        return False


class Wyspa:
    def __init__(self, nazwa, x, y, bazy, strefy):
        self.nazwa = nazwa.strip()
        self.x = x
        self.y = y
        self.bazy = bazy
        self.strefy = strefy
        self.odcinki = []  # sa to polaczenia miedzy punktami na wyspie
        for baza in self.bazy:
            baza.wyspa = self
        for strefa in self.strefy:
            strefa.wyspa = self
            strefa.punkt_a.wyspa = self
            strefa.punkt_b.wyspa = self
            strefa.punkt_c.wyspa = self
            strefa.punkt_d.wyspa = self
        if len(bazy) > 1:
            for baza in bazy:
                baza.lista_polaczen_posrednich = self.wyznacz_droge_wewnatrz_wyspy(baza)

    def zwroc_wszystkie_punkty(self):
        lista_wszystkich_punktow = []
        for baza in self.bazy:
            lista_wszystkich_punktow.append(baza)
        for strefa in self.strefy:
            for punkt in strefa.zwroc_punkty():
                lista_wszystkich_punktow.append(punkt)
        return lista_wszystkich_punktow

    def tworz_liste_polaczen_bezposrednich_wewnatrz_wyspy(self):
        if len(self.odcinki) == 0:
            punkty = []
            for baza in self.bazy:
                punkty.append(baza)
            for strefa in self.strefy:
                for punkt in strefa.zwroc_punkty():
                    punkty.append(punkt)
            pary = (filter(lambda para: not Odcinek(para[0], para[1]).czy_odcinek_przecina_jakies_strefy(self.strefy),
                           combinations(punkty, 2)))
            self.odcinki = [Odcinek(para[0], para[1], True) for para in pary]
            for odcinek in self.odcinki:
                odcinek.punkt_a.odcinki.append(odcinek)
                odcinek.punkt_b.odcinki.append(odcinek)
        return self.odcinki

    @staticmethod
    def wyznacz_droge(wyspy, trasa, przypadek):
        baza_1, wyspa_1, baza_2, wyspa_2 = trasa
        baza_1_zidentyfikowana = None
        baza_2_zidentyfikowana = None
        for wyspa in wyspy:
            if wyspa.nazwa.strip() == wyspa_1:
                for baza in wyspa.bazy:
                    if baza.nazwa.strip() == baza_1:
                        baza_1_zidentyfikowana = baza
                        # print("znalazlem dopasowanie bazy 1", baza_1_zidentyfikowana.drukuj())
                        break
            if wyspa.nazwa.strip() == wyspa_2:
                for baza in wyspa.bazy:
                    if baza.nazwa.strip() == baza_2:
                        baza_2_zidentyfikowana = baza
                        # print("znalazlem dopasowanie bazy 1", baza_2_zidentyfikowana.drukuj())
                        break
        if baza_1_zidentyfikowana.wyspa == baza_2_zidentyfikowana.wyspa:
            polaczenie = baza_1_zidentyfikowana.lista_polaczen_posrednich[baza_2_zidentyfikowana.index]
            print("case", przypadek, "Y")
            print(polaczenie.dystans)
            print(polaczenie.punkt_poczatkowy.drukuj())
            polaczenie.wyswietl_trase()
        else:
            polaczenie = Wyspa.wyznacz_droge_miedzy_wyspami(wyspy, baza_1_zidentyfikowana, baza_2_zidentyfikowana)
            print("case", przypadek, "Y")
            print(polaczenie.dystans)
            print(polaczenie.punkt_poczatkowy.drukuj())
            polaczenie.wyswietl_trase()
            # print(polaczenie.punkt_docelowy.drukuj())

    @staticmethod
    def wyznacz_droge_miedzy_wyspami(wyspy, punkt_poczatkowy, punkt_docelowy):
        bazy_wszystkie_do_przetworzenia = []
        lista_polaczen_globalnych = []
        for wyspa in wyspy:
            bazy_wszystkie_do_przetworzenia += wyspa.bazy
        for index, baza in enumerate(bazy_wszystkie_do_przetworzenia):
            lista_polaczen_globalnych.append(TrasaGlobalna(punkt_poczatkowy, baza))
            baza.index_globalny = index
        lista_polaczen_globalnych[punkt_poczatkowy.index_globalny].dystans = 0
        bazy_przetworzone = []
        bazy_do_przetworzenia_w_nastepnej_kolejce = [punkt_poczatkowy]
        while bazy_do_przetworzenia_w_nastepnej_kolejce:
            biezace_bazy_do_przetworzenia = sorted(bazy_do_przetworzenia_w_nastepnej_kolejce,
                                                   key=lambda x: lista_polaczen_globalnych[x.index_globalny].dystans)
            bazy_do_przetworzenia_w_nastepnej_kolejce = []
            for baza in biezace_bazy_do_przetworzenia:
                polaczenia_do_przetworzenia = baza.polaczenia_wewnetrzne + baza.polaczenia_zewnetrzne
                for polaczenie in polaczenia_do_przetworzenia:
                    if polaczenie.punkt_poczatkowy == baza:
                        baza_posrednia = polaczenie.punkt_docelowy
                    else:  # polaczenie.baza_2 == baza:
                        baza_posrednia = polaczenie.punkt_poczatkowy
                    trasa = TrasaGlobalna(punkt_poczatkowy, baza_posrednia,
                                          lista_polaczen_globalnych[baza.index_globalny], polaczenie,
                                          lista_polaczen_globalnych[baza.index_globalny].dystans + polaczenie.dystans)
                    lista_polaczen_globalnych[
                        baza_posrednia.index_globalny] = trasa.porownaj_trasy_zwroc_optymalniejsza(
                        lista_polaczen_globalnych[baza_posrednia.index_globalny])
                    if (baza_posrednia not in bazy_do_przetworzenia_w_nastepnej_kolejce) and (
                            baza_posrednia not in bazy_przetworzone):
                        bazy_do_przetworzenia_w_nastepnej_kolejce.append(baza_posrednia)
            nowa_lista_baz_wszystkich = []
            for baza_do_przekazania in bazy_wszystkie_do_przetworzenia:
                if baza_do_przekazania not in biezace_bazy_do_przetworzenia:
                    nowa_lista_baz_wszystkich.append(baza_do_przekazania)
                else:
                    bazy_przetworzone.append(baza_do_przekazania)
            bazy_wszystkie_do_przetworzenia = nowa_lista_baz_wszystkich
        return lista_polaczen_globalnych[punkt_docelowy.index_globalny]

    def wyznacz_droge_wewnatrz_wyspy(self, punkt_bazowy):
        self.tworz_liste_polaczen_bezposrednich_wewnatrz_wyspy()
        lista_polaczen_posrednich = []
        punkty_wszystkie_do_przetworzenia = self.zwroc_wszystkie_punkty()
        for index, punkt in enumerate(punkty_wszystkie_do_przetworzenia):
            lista_polaczen_posrednich.append(Trasa(punkt_bazowy, punkt))
            punkt.index = index
        lista_polaczen_posrednich[punkt_bazowy.index].dystans = 0
        punkty_przetworzone = []
        punkty_do_przetworzenia_w_nastepnej_kolejce = [punkt_bazowy]
        while punkty_do_przetworzenia_w_nastepnej_kolejce:
            biezace_punkty_do_przetworzenia = sorted(punkty_do_przetworzenia_w_nastepnej_kolejce,
                                                     key=lambda x: lista_polaczen_posrednich[x.index].dystans)
            punkty_do_przetworzenia_w_nastepnej_kolejce = []
            for punkt in biezace_punkty_do_przetworzenia:
                polaczenia_do_przetworzenia = punkt.odcinki
                for polaczenie in polaczenia_do_przetworzenia:
                    punkt_posredni = punkt
                    if polaczenie.punkt_a == punkt:
                        punkt_posredni = polaczenie.punkt_b
                    else:  # polaczenie.punkt_b == punkt:
                        punkt_posredni = polaczenie.punkt_a
                    trasa = Trasa(punkt_bazowy, punkt_posredni, lista_polaczen_posrednich[punkt.index], polaczenie,
                                  lista_polaczen_posrednich[punkt.index].dystans + polaczenie.dlugosc())
                    lista_polaczen_posrednich[punkt_posredni.index] = trasa.porownaj_trasy_zwroc_optymalniejsza(
                        lista_polaczen_posrednich[punkt_posredni.index])
                    if (punkt_posredni not in punkty_do_przetworzenia_w_nastepnej_kolejce) and (
                            punkt_posredni not in punkty_przetworzone):
                        punkty_do_przetworzenia_w_nastepnej_kolejce.append(punkt_posredni)
            nowa_lista_punktow_wszystkich = []
            for punkt_do_przekazania in punkty_wszystkie_do_przetworzenia:
                if punkt_do_przekazania not in biezace_punkty_do_przetworzenia:
                    nowa_lista_punktow_wszystkich.append(punkt_do_przekazania)
                else:
                    punkty_przetworzone.append(punkt_do_przekazania)
            punkty_wszystkie_do_przetworzenia = nowa_lista_punktow_wszystkich
        for baza in self.bazy:
            lista_polaczen_posrednich[baza.index].dystans = ceil(lista_polaczen_posrednich[baza.index].dystans)
            punkt_bazowy.polaczenia_wewnetrzne.append(lista_polaczen_posrednich[baza.index])
        return lista_polaczen_posrednich  # usunalem dopisek: [punkt_docelowy.index]


def main():
    liczba_przypadkow = int(input())
    przypadek = 1
    while liczba_przypadkow > 0:
        try:
            liczba_wysp = int(input())
            wyspy = []
            while liczba_wysp > 0:
                nazwa_wyspy = input().strip()
                wymiar_x, wymiar_y = input().split()
                liczba_baz = int(input())
                bazy = []
                while liczba_baz > 0:
                    nazwa_bazy, x, y = input().split()
                    liczba_baz -= 1
                    bazy.append(Baza(float(x.replace(",", ".")), float(y.replace(",", ".")), nazwa_bazy.strip(), None))
                liczba_stref = int(input())
                strefy = []
                while liczba_stref > 0:
                    x_1, y_1, x_2, y_2 = input().split()
                    liczba_stref -= 1
                    strefy.append(Strefa(float(x_1.replace(",", ".")), float(y_1.replace(",", ".")),
                                         float(x_2.replace(",", ".")), float(y_2.replace(",", ".")), None))
                wyspa = Wyspa(nazwa_wyspy.strip(), float(wymiar_x.replace(",", ".")), float(wymiar_y.replace(",", ".")), bazy, strefy)
                for baza in wyspa.bazy:
                    baza.wyspa = wyspa
                for strefa in wyspa.strefy:
                    strefa.wyspa = wyspa
                wyspy.append(wyspa)
                liczba_wysp -= 1
            liczba_polaczen = int(input())
            while liczba_polaczen > 0:
                dane_wejsciowe = input()
                PolaczenieMiedzywyspowe.wczytaj_dane_polaczenia(wyspy, dane_wejsciowe)
                liczba_polaczen -= 1
            trasa_do_pokonania = input().split()
            Wyspa.wyznacz_droge(wyspy, trasa_do_pokonania, przypadek)
            print()
        except (ValueError, AttributeError):
            print("case", przypadek, "N")
        liczba_przypadkow -= 1
        przypadek += 1


if __name__ == "__main__":
    main()
