# Aplikacja biblioteczna OOP
# Autor: Kacper Kossakowski
# 160614


class Book:
    def __init__(self, title, author, total_copies):
        self.title = title
        self.author = author
        self._total_copies = total_copies
        self._available_copies = total_copies

    @property
    def available_copies(self):
        return self._available_copies

    @property
    def total_copies(self):
        return self._total_copies

    def borrow(self):
        if self._available_copies <= 0:
            return False
        self._available_copies -= 1
        return True

    def return_book(self):
        if self._available_copies < self._total_copies:
            self._available_copies += 1

    def __str__(self):
        return f"{self.title} - {self.author} (dostepne: {self._available_copies}/{self._total_copies})"


class User:
    def __init__(self, login, password, role):
        self.login = login
        self._password = password
        self.role = role

    def authenticate(self, password):
        return self._password == password


class Reader(User):
    def __init__(self, login, password):
        super().__init__(login, password, "czytelnik")
        self.borrowed_books = []
        self.extension_requests = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def has_book(self, title):
        for book in self.borrowed_books:
            if book.title.lower() == title.lower():
                return True
        return False

    def request_extension(self, book):
        self.extension_requests.append(book)


class Librarian(User):
    def __init__(self, login, password):
        super().__init__(login, password, "bibliotekarz")


class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.extension_queue = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def find_user(self, login):
        for user in self.users:
            if user.login == login:
                return user
        return None

    def find_book(self, title):
        title = title.strip().lower()
        for book in self.books:
            if book.title.lower() == title:
                return book
        return None

    def login_user(self):
        max_attempts = 3

        for attempt in range(max_attempts):
            print("\n=== LOGOWANIE ===")
            login = input("Podaj login: ").strip()
            password = input("Podaj haslo: ").strip()

            user = self.find_user(login)

            if user is not None and user.authenticate(password):
                print(f"\nZalogowano pomyslnie. Witaj, {user.login}!")
                return user

            print("Niepoprawny login lub haslo.")
            remaining = max_attempts - attempt - 1

            if remaining > 0:
                print(f"Pozostalo prob: {remaining}")

        print("\nPrzekroczono limit prob logowania.")
        return None

    def show_catalog(self):
        print("\n=== KATALOG KSIAZEK ===")

        if len(self.books) == 0:
            print("Brak ksiazek w katalogu.")
            return

        for index, book in enumerate(self.books, start=1):
            print(f"{index}. {book}")

    def borrow_book(self, reader):
        print("\n=== WYPOZYCZANIE KSIAZKI ===")
        title = input("Podaj tytul ksiazki: ").strip()

        book = self.find_book(title)

        if book is None:
            print("Nie znaleziono ksiazki o podanym tytule.")
            return

        if reader.has_book(book.title):
            print("Masz juz wypozyczona te ksiazke.")
            return

        if book.borrow():
            reader.borrow_book(book)
            print(f'Ksiazka "{book.title}" zostala wypozyczona pomyslnie.')
        else:
            print("Brak dostepnych sztuk tej ksiazki.")

    def show_reader_books(self, reader):
        print("\n=== MOJE WYPOZYCZENIA ===")

        if len(reader.borrowed_books) == 0:
            print("Nie masz obecnie zadnych wypozyczonych ksiazek.")
            return

        for index, book in enumerate(reader.borrowed_books, start=1):
            print(f"{index}. {book.title}")

    def create_extension_request(self, reader):
        print("\n=== PROSBA O PRZEDLUZENIE ===")

        if len(reader.borrowed_books) == 0:
            print("Nie masz ksiazek do przedluzenia.")
            return

        self.show_reader_books(reader)
        title = input("Podaj tytul ksiazki do przedluzenia: ").strip()

        for book in reader.borrowed_books:
            if book.title.lower() == title.lower():
                request = {
                    "reader": reader,
                    "book": book
                }

                self.extension_queue.append(request)
                reader.request_extension(book)

                print(f'Prosba o przedluzenie ksiazki "{book.title}" zostala wyslana.')
                return

        print("Nie masz wypozyczonej ksiazki o takim tytule.")

    def show_all_borrowings(self):
        print("\n=== WSZYSTKIE WYPOZYCZENIA ===")
        found = False

        for user in self.users:
            if isinstance(user, Reader):
                for book in user.borrowed_books:
                    print(f"{user.login} -> {book.title}")
                    found = True

        if not found:
            print("Brak aktualnych wypozyczen.")

    def handle_extension_requests(self):
        print("\n=== OBSLUGA PROSB O PRZEDLUZENIE ===")

        if len(self.extension_queue) == 0:
            print("Brak prosb o przedluzenie.")
            return

        index = 0

        while index < len(self.extension_queue):
            request = self.extension_queue[index]
            reader = request["reader"]
            book = request["book"]

            print(f"\nProsba {index + 1}:")
            print(f"Czytelnik: {reader.login}")
            print(f"Ksiazka: {book.title}")

            decision = input("Zaakceptowac prosbe? (t/n): ").strip().lower()

            if decision == "t":
                print("Prosba zostala zaakceptowana.")
                self.extension_queue.pop(index)
            elif decision == "n":
                print("Prosba zostala odrzucona.")
                self.extension_queue.pop(index)
            else:
                print("Niepoprawna decyzja. Przechodze do kolejnej prosby.")
                index += 1

    def reader_menu(self, reader):
        while True:
            print("\n=== MENU CZYTELNIKA ===")
            print("1. Przegladaj katalog")
            print("2. Wypozycz ksiazke")
            print("3. Moje wypozyczenia")
            print("4. Prosba o przedluzenie")
            print("5. Wyloguj")

            choice = input("Wybierz opcje: ").strip()

            if choice == "1":
                self.show_catalog()
            elif choice == "2":
                self.borrow_book(reader)
            elif choice == "3":
                self.show_reader_books(reader)
            elif choice == "4":
                self.create_extension_request(reader)
            elif choice == "5":
                print(f"Wylogowano uzytkownika {reader.login}.")
                break
            else:
                print("Niepoprawny wybor.")

    def librarian_menu(self, librarian):
        while True:
            print("\n=== MENU BIBLIOTEKARZA ===")
            print("1. Przegladaj katalog")
            print("2. Lista wypozyczen")
            print("3. Obsluga prosb o przedluzenie")
            print("4. Wyloguj")

            choice = input("Wybierz opcje: ").strip()

            if choice == "1":
                self.show_catalog()
            elif choice == "2":
                self.show_all_borrowings()
            elif choice == "3":
                self.handle_extension_requests()
            elif choice == "4":
                print(f"Wylogowano uzytkownika {librarian.login}.")
                break
            else:
                print("Niepoprawny wybor.")

    def run(self):
        user = self.login_user()

        if user is None:
            return

        if isinstance(user, Reader):
            self.reader_menu(user)
        elif isinstance(user, Librarian):
            self.librarian_menu(user)


def prepare_library():
    library = Library()

    library.add_book(Book("Lalka", "Boleslaw Prus", 3))
    library.add_book(Book("Pan Tadeusz", "Adam Mickiewicz", 2))
    library.add_book(Book("Zbrodnia i kara", "Fiodor Dostojewski", 4))
    library.add_book(Book("Rok 1984", "George Orwell", 1))
    library.add_book(Book("Wiedzmin: Ostatnie zyczenie", "Andrzej Sapkowski", 5))

    library.add_user(Reader("anna", "anna123"))
    library.add_user(Reader("tomek", "tomek123"))
    library.add_user(Reader("kasia", "kasia123"))
    library.add_user(Librarian("admin", "admin123"))

    return library


def main():
    library = prepare_library()
    library.run()


main()