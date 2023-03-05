import sqlite3


class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"{self.title} by {self.author}, {self.year}"


class Library:
    def __init__(self, db_name):
        """
        Connects to an SQLite database and creates a connection and cursor object.

        :param db_name: the name of the SQLite database to use.
        """
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def add_book(self, book):
        """
        Adds a book to the library.

        :param book: the book object to add.
        """
        self.c.execute(
            "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
            (book.title, book.author, book.year),
        )
        self.conn.commit()

    def remove_book(self, book):
        """
        Removes a book from the library.

        :param book: the book object to remove.
        """
        self.c.execute(
            "DELETE FROM books WHERE title=? AND author=? AND year=?",
            (book.title, book.author, book.year),
        )
        self.conn.commit()

    def update_book(self, old_book, new_book):
        """
        Updates the information of a book in the library.

        :param old_book: the old book object to update.
        :param new_book: the new book object to update to.
        """
        self.c.execute(
            "UPDATE books SET title=?, author=?, year=? WHERE title=? AND author=? AND year=?",
            (
                new_book.title,
                new_book.author,
                new_book.year,
                old_book.title,
                old_book.author,
                old_book.year,
            ),
        )
        self.conn.commit()

    def get_books(self):
        """
        Gets all the books in the library.

        :return: a list of book objects.
        """
        self.c.execute("SELECT * FROM books")
        books = []
        for row in self.c.fetchall():
            book = Book(row[1], row[2], row[3])
            books.append(book)
        return books

    def __del__(self):
        """
        Closes the SQLite connection.
        """
        self.conn.close()
