from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def f_dij(self, napok_szama):
        return self.ar * napok_szama


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar=4000):
        super().__init__(ar, szobaszam)

    def f_dij(self, napok_szama):
        return super().f_dij(napok_szama)


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar=7000):
        super().__init__(ar, szobaszam)

    def f_dij(self, napok_szama):
        return super().f_dij(napok_szama)


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def f_lemondas(self, szobaszam, kezdet):
        for i, foglalas in enumerate(self.foglalasok):
            if foglalas.szobaszam == szobaszam and foglalas.kezdet == kezdet:
                del self.foglalasok[i]
                return True, "Foglalás lemondva."
        return False, "Nincs ilyen foglalás."

    def sz_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def sz_listazas(self):
        if not self.szobak:
            return "Jelenleg nincsenek szobák a szállodában."
        return "\n".join(
            f"Szobaszám: {szoba.szobaszam}, Típus: {'Egyágyas' if isinstance(szoba, EgyagyasSzoba) else 'Kétágyas'}"
            for szoba in self.szobak)

    def f_hozzadas(self, szobaszam, kezdet, vege):
        if vege <= kezdet:
            return None, "A foglalás végének a dátum nem lehet korábbi, mint a foglalás kezdetének a dátumával."
        if any(f.szobaszam == szobaszam and not (f.vege <= kezdet or f.kezdet >= vege) for f in self.foglalasok):
            return None, "A szoba már foglalt ebben az időszakban."
        if kezdet < datetime.now():
            return None, "A foglalás kezdetének a dátuma nem lehet a múltban."

        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                napok = (vege - kezdet).days + 1
                dij = szoba.f_dij(napok)
                self.foglalasok.append(Foglalas(szobaszam, kezdet, vege))
                return dij, "Foglalás sikeresen létrehozva, a foglalás ára: {} Ft".format(dij)

        return None, "Nem található a szobaszám ."

    def f_listazas(self):
        if not self.foglalasok:
            return "Nincsenek aktív foglalások."
        return "\n".join(
            f"Szobaszám: {f.szobaszam}, Kezdet: {f.kezdet.date()}, Vége: {f.vege.date()}" for f in self.foglalasok)


class Foglalas:
    def __init__(self, szobaszam, kezdet, vege):
        self.szobaszam = szobaszam
        self.kezdet = kezdet
        self.vege = vege


def cli(szalloda):
    while True:
        print("\n1 - Foglalás")
        print("2 - Foglalás lemondása")
        print("3 - Foglalások listázása")
        print("4 - Szobák listázása")
        print("5 - Kilépés")
        valasztas = input("Válasszon egy opciót: ")

        if valasztas == "1":
            szobaszam = int(input("Adja meg a szobaszámot: "))
            kezdet = datetime.strptime(input("Adja meg a foglalás kezdetének a dátumát : YYYY-MM-DD: "), "%Y-%m-%d")
            vege = datetime.strptime(input("Adja meg a foglalás végének a dátumát: YYYY-MM-DD: "), "%Y-%m-%d")
            dij, uzenet = szalloda.f_hozzadas(szobaszam, kezdet, vege)
            print(uzenet)

        elif valasztas == "2":
            szobaszam = int(input("Adja meg a szobaszámot: "))
            kezdet = datetime.strptime(input("Adja meg a foglalás kezdetének a dátumát: YYYY-MM-DD: "), "%Y-%m-%d")
            siker, uzenet = szalloda.f_lemondas(szobaszam, kezdet)
            print(uzenet)

        elif valasztas == "3":
            print(szalloda.f_listazas())

        elif valasztas == "4":

            print(szalloda.sz_listazas())

        elif valasztas == "5":

            break
        else:
            print("Érvénytelen opció, próbálja újra!")



# Szálloda és szobák inicializálása
szalloda = Szalloda("Példa Szálloda")
szalloda.sz_hozzaadas(EgyagyasSzoba(101))
szalloda.sz_hozzaadas(KetagyasSzoba(102))
szalloda.sz_hozzaadas(KetagyasSzoba(103))

# Foglalások előkészítése
now = datetime.now()
future_dates = [now + timedelta(days=i * 10) for i in range(1, 6)]
for i in range(5):
    szalloda.f_hozzadas(101 + i % 3, future_dates[i], future_dates[i] + timedelta(days=2))

# Felhasználói interfész indítása
cli(szalloda)
