#Aplikacja biblioteczna
#Autor:
#Kacper Kossakowski
#160614

def przygotuj_ksiazki():
    return [
        {"tytul": "Lalka", "autor": "Boleslaw Prus", "dostepne_sztuki": 3},
        {"tytul": "Pan Tadeusz", "autor": "Adam Mickiewicz", "dostepne_sztuki": 2},
        {"tytul": "Zbrodnia i kara", "autor": "Fiodor Dostojewski", "dostepne_sztuki": 4},
        {"tytul": "Rok 1984", "autor": "George Orwell", "dostepne_sztuki": 1},
        {"tytul": "Wiedzmin: Ostatnie zyczenie", "autor": "Andrzej Sapkowski", "dostepne_sztuki": 5},
    ]


def przygotuj_uzytkownikow():
    return [
        {
            "login": "anna",
            "haslo": "anna123",
            "rola": "czytelnik",
            "wypozyczenia": []
        },
        {
            "login": "tomek",
            "haslo": "tomek123",
            "rola": "czytelnik",
            "wypozyczenia": []
        },
        {
            "login": "kasia",
            "haslo": "kasia123",
            "rola": "czytelnik",
            "wypozyczenia": []
        },
    ]


def znajdz_uzytkownika(login, uzytkownicy):
    for uzytkownik in uzytkownicy:
        if uzytkownik["login"] == login:
            return uzytkownik
    return None


def zaloguj_uzytkownika(uzytkownicy):
    maks_liczba_prob = 3
    liczba_prob = 0

    while liczba_prob < maks_liczba_prob:
        print("\n=== LOGOWANIE ===")
        login = input("Podaj login: ").strip()
        haslo = input("Podaj haslo: ").strip()

        uzytkownik = znajdz_uzytkownika(login, uzytkownicy)

        if uzytkownik is not None and uzytkownik["haslo"] == haslo:
            print(f"\nZalogowano pomyslnie. Witaj, {uzytkownik['login']}!")
            return uzytkownik

        liczba_prob += 1
        pozostale_proby = maks_liczba_prob - liczba_prob
        print("Niepoprawny login lub haslo.")

        if pozostale_proby > 0:
            print(f"Pozostalo prob: {pozostale_proby}")

    print("\nPrzekroczono limit prob logowania. Program zostanie zakonczony.")
    return None


def wyswietl_menu():
    print("\n=== MENU GLOWNE ===")
    print("1. Przegladaj katalog")
    print("2. Wypozycz ksiazke")
    print("3. Moje wypozyczenia")
    print("4. Wyloguj")


def wyswietl_katalog(ksiazki):
    print("\n=== KATALOG KSIAZEK ===")

    if len(ksiazki) == 0:
        print("Brak ksiazek w katalogu.")
        return

    for indeks, ksiazka in enumerate(ksiazki, start=1):
        print(
            f"{indeks}. {ksiazka['tytul']} - {ksiazka['autor']} "
            f"(dostepne sztuki: {ksiazka['dostepne_sztuki']})"
        )


def znajdz_ksiazke_po_tytule(tytul, ksiazki):
    tytul_szukany = tytul.strip().lower()

    for ksiazka in ksiazki:
        if ksiazka["tytul"].lower() == tytul_szukany:
            return ksiazka

    return None


def czy_uzytkownik_ma_juz_ta_ksiazke(uzytkownik, tytul_ksiazki):
    for wypozyczona_ksiazka in uzytkownik["wypozyczenia"]:
        if wypozyczona_ksiazka.lower() == tytul_ksiazki.lower():
            return True
    return False


def wypozycz_ksiazke(uzytkownik, ksiazki):
    print("\n=== WYPOZYCZANIE KSIAZKI ===")
    tytul = input("Podaj tytul ksiazki: ").strip()

    ksiazka = znajdz_ksiazke_po_tytule(tytul, ksiazki)

    if ksiazka is None:
        print("Nie znaleziono ksiazki o podanym tytule.")
        return

    if ksiazka["dostepne_sztuki"] <= 0:
        print("Brak dostepnych sztuk tej ksiazki.")
        return

    if czy_uzytkownik_ma_juz_ta_ksiazke(uzytkownik, ksiazka["tytul"]):
        print("Masz juz wypozyczona te ksiazke.")
        return

    ksiazka["dostepne_sztuki"] -= 1
    uzytkownik["wypozyczenia"].append(ksiazka["tytul"])

    print(f'Ksiazka "{ksiazka["tytul"]}" zostala wypozyczona pomyslnie.')


def wyswietl_moje_wypozyczenia(uzytkownik):
    print("\n=== MOJE WYPOZYCZENIA ===")

    if len(uzytkownik["wypozyczenia"]) == 0:
        print("Nie masz obecnie zadnych wypozyczonych ksiazek.")
        return

    for indeks, tytul in enumerate(uzytkownik["wypozyczenia"], start=1):
        print(f"{indeks}. {tytul}")


def obsluz_menu_uzytkownika(uzytkownik, ksiazki):
    while True:
        wyswietl_menu()
        wybor = input("Wybierz opcje: ").strip()

        if wybor == "1":
            wyswietl_katalog(ksiazki)
        elif wybor == "2":
            wypozycz_ksiazke(uzytkownik, ksiazki)
        elif wybor == "3":
            wyswietl_moje_wypozyczenia(uzytkownik)
        elif wybor == "4":
            print(f"Wylogowano uzytkownika {uzytkownik['login']}.")
            break
        else:
            print("Niepoprawny wybor. Sprobuj ponownie.")


def main():
    ksiazki = przygotuj_ksiazki()
    uzytkownicy = przygotuj_uzytkownikow()

    zalogowany_uzytkownik = zaloguj_uzytkownika(uzytkownicy)

    if zalogowany_uzytkownik is None:
        return

    obsluz_menu_uzytkownika(zalogowany_uzytkownik, ksiazki)


main()