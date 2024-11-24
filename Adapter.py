import csv
####################################################Adapter####################################
class Adapter:
    def __init__(self, sciezka_pliku):
        self.sciezka_pliku = sciezka_pliku

    def wczytaj_dane(self):
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