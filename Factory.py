## Zaimplementuj UserFactory,
## która tworzy różne typy obiektów użytkowników (np. Student, Nauczyciel, Bibliotekarz) na podstawie danych wejściowych.
## Każdy typ użytkownika może mieć różne uprawnienia do wypożyczania książek."""

####################################Fac tory###########################################

class User:
    def __init__(self, imie, typ):
        self.imie = imie
        self.typ = typ

    def przedstaw(self):
        print(f"Jestem {self.imie}, typ: {self.typ}")


class UserFactory:
    @staticmethod
    def stworz_u(imie, typ):
        return User(imie, typ)


# Test
student = UserFactory.stworz_u("Jan k", "Student")
nauczyciel = UserFactory.stworz_u("Jan B", "Nauczyciel")

student.przedstaw()
nauczyciel.przedstaw()

###############################################################