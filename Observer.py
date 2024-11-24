"""Skonfiguruj system powiadomień, w którym użytkownicy mogą zapisywać się na powiadomienia o wypożyczeniu lub zwrocie książek. 
LibraryCatalog będzie działał jako podmiot, a użytkownicy jako obserwatorzy."""
class Observer:
    def __init__(self):
        self.obserwatorzy = []
        self.ksiazki = []

    def dodaj_obserwatora(self, obserwator):
        self.obserwatorzy.append(obserwator)

    def powiadom_obserwatorow(self, tytul):
        for obserwator in self.obserwatorzy:
            obserwator.powiadom(tytul)

    def dodaj_ksiazke(self, tytul):
        self.ksiazki.append(tytul)
        print(f"Dodano ksiazkę: {tytul}")
        self.powiadom_obserwatorow(tytul)


class User:
    def __init__(self, imie):
        self.imie = imie

    def powiadom(self, tytul):
        print(f"{self.imie} ksiazka '{tytul}' jest dostępna")


# Test
katalog = Observer()
uzytkownik1 = User("Jan M")
uzytkownik2 = User("Jan C")

katalog.dodaj_obserwatora(uzytkownik1)
katalog.dodaj_obserwatora(uzytkownik2)

katalog.dodaj_ksiazke("Hobbit")