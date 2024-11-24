#Zaimplementuj klasę LibraryCatalog, która zapewnia, że w programie istnieje tylko jedna instancja katalogu.
#Klasa ta będzie odpowiedzialna za przechowywanie i zarządzanie danymi o książkach.
#

class LibraryCatalog:
    _instancja = None #Pole służące do przechowywania instancji singleton powinno

    def __new__(cls, *args, **kwargs): #tworzenie nowej instancji - Jeśli instancja już istnieje  zwraca ją zamiast tworzyć nową
        if not cls._instancja:
            cls._instancja = super().__new__(cls)
            cls._instancja.ksiazki = []
        return cls._instancja

    def dodaj_ksiazke(self, tytul):
        self.ksiazki.append(tytul)
        print(f"Dodano książkę: {tytul}")

    def wyswietl_ksiazki(self):
        print("Książki w katalogu:")
        for ksiazka in self.ksiazki:
            print(f"- {ksiazka}")


# Test
katalog1 = LibraryCatalog()
katalog1.dodaj_ksiazke("Miasteczko dobrych dusz")
katalog2 = LibraryCatalog()
katalog2.wyswietl_ksiazki()
print("Czy katalog1 to katalog2:", katalog1 is katalog2)
#test 2 
if id(katalog1) == id(katalog2):
    print("Tak")
else:
    print("Nie")
###############################################################################################