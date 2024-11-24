#"""Wyobraź sobie, że system biblioteczny musi importować dane o książkach z różnych formatów 
#(np. JSON, CSV). Stwórz klasę adaptera,
# która pozwoli na przetwarzanie i integrację różnych formatów danych do standardowego formatu używanego w LibraryCatalog"""

import csv
####################################################Adapter####################################
class Adapter:# przyjmuje ścieżkę do pliku CSV
    def __init__(self, sciezka_pliku):
        self.sciezka_pliku = sciezka_pliku

    def wczytaj_dane(self): #odczytuje tytuły książek z cvs
        ksiazki = []
        with open(self.sciezka_pliku, newline='') as plik:
            reader = csv.reader(plik)
            for wiersz in reader:
                ksiazki.append(wiersz[0])  
        return ksiazki


# Test
with open("C:/Users/Public/Desktop/test.csv", "w") as plik:

    plik.write("Harry Potter\nWładca Pierścieni")

adapter = Adapter("C:/Users/Public/Desktop/test.csv")
ksiazki_csv = adapter.wczytaj_dane()
print("Wczytane książki:", ksiazki_csv)
######################################################################################