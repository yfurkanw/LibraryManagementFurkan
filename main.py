
import sqlite3

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f'{self.title} by {self.author}, {self.year}'


class Library:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def add_book(self, book):
        self.c.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (book.title, book.author, book.year))
        self.conn.commit()

    def remove_book(self, book):
        self.c.execute('DELETE FROM books WHERE title=? AND author=? AND year=?', (book.title, book.author, book.year))
        self.conn.commit()

    def update_book(self, old_book, new_book):
        self.c.execute('UPDATE books SET title=?, author=?, year=? WHERE title=? AND author=? AND year=?', 
                        (new_book.title, new_book.author, new_book.year, old_book.title, old_book.author, old_book.year))
        self.conn.commit()

    def get_books(self):
        self.c.execute('SELECT * FROM books')
        books = []
        for row in self.c.fetchall():
            book = Book(row[1], row[2], row[3])
            books.append(book)
        return books

    def __del__(self):
        self.conn.close()