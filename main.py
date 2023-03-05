import sqlite3


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'User({self.name}, {self.email})'


class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
        self.status = 'available'

    def __repr__(self):
        return f'Book({self.title}, {self.author}, {self.pages}, {self.status})'


class Library:
    def __init__(self, name, books):
        self.name = name
        self.books = books
        
        # Veritabanı bağlantısı oluşturuluyor ve tablo varsa oluşturulması sağlanıyor.
        self.db_connection = sqlite3.connect('library.db')
        self.db_cursor = self.db_connection.cursor()
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS books
                                 (id INTEGER PRIMARY KEY,
                                  title TEXT,
                                  author TEXT,
                                  pages INTEGER,
                                  status TEXT)''')

    def __repr__(self):
        return f'Library({self.name}, {len(self.books)} books)'

    def add_book(self, book):
        """
        Adds a book to the library.

        :param book: The book object to add.
        """
        self.books.append(book)
        
        # Kitap verileri veritabanına ekleniyor.
        self.db_cursor.execute(f"INSERT INTO books VALUES (null, '{book.title}', '{book.author}', {book.pages}, '{book.status}')")
        self.db_connection.commit()

    def delete_book(self, book):
        """
        Deletes a book from the library.

        :param book: The book object to delete.
        """
        self.books.remove(book)
        
        # Kitap verileri veritabanından siliniyor.
        self.db_cursor.execute(f"DELETE FROM books WHERE title='{book.title}'")
        self.db_connection.commit()

    def update_book_status(self, book, new_status):
        """
        Updates the status of a book in the library.

        :param book: The book object to update.
        :param new_status: The new status to set for the book.
        """
        book.status = new_status
        
        # Kitap durumu veritabanında güncelleniyor.
        self.db_cursor.execute(f"UPDATE books SET status='{new_status}' WHERE title='{book.title}'")
        self.db_connection.commit()

    def list_books(self):
        """
        Lists all books in the library.

        :return: A list of Book objects.
        """
        # Tüm kitaplar veritabanından çekilip kitap nesnesine dönüştürülüyor.
        self.db_cursor.execute("SELECT * FROM books")
        rows = self.db_cursor.fetchall()
        books = []
        for row in rows:
            title, author, pages, status = row[1:]
            book = Book(title, author, pages)
            book.status = status
            books.append(book)
            
        # Kitap listesi güncelleniyor ve döndürülüyor.
        self.books = books
        return self.books


class UserFactory:
    def create_user(self, name, email):
        """
        Creates a new User object.

        :param name: The name of the user.
        :param email: The email address of the user.
        :return: A new User object.
        """

def main():
    # User Input
    name = input("Enter user name: ")
    email = input("Enter user email: ")
    user_factory = UserFactory()
    user = user_factory.create_user(name, email)

    # Library starting
    library = Library("My Library", [])

    # menü
    while True:
        print("\nChoose an option:")
        print("1. Add a book")
        print("2. Delete a book")
        print("3. List books")
        print("4. Quit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            # Book information taking from user
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            pages = int(input("Enter number of pages: "))

            # New book
            book = Book(title, author, pages)
            library.add_book(book)
            print(f"Book '{book.title}' added to the library.")

        elif choice == "2":
            # Book information taking from user
            title = input("Enter book title: ")
            author = input("Enter book author: ")

            # If book in library, it is deleting
            books_to_delete = [book for book in library.list_books() if book.title == title and book.author == author]
            if books_to_delete:
                for book in books_to_delete:
                    library.delete_book(book)
                print(f"{len(books_to_delete)} books deleted from the library.")
            else:
                print("No book found with that title and author.")

        elif choice == "3":
            # It showing list of books
            books = library.list_books()
            if books:
                print("Books in the library:")
                for book in books:
                    print(book)
            else:
                print("No books in the library.")

        elif choice == "4":
            # Exiting
            print("Goodbye!")
            break

        else:
            # Hatalı giriş yapılırsa uyarı veriliyor
            print("Invalid choice. Please enter a number between 1 and 4.")


main()