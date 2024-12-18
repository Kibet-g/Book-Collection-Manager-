#!/usr/bin/env python3

import os
import sys
from subprocess import call
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Database Setup
Base = declarative_base()
engine = create_engine('sqlite:///books.db')  # SQLite database
Session = sessionmaker(bind=engine)

# Models
class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    books = relationship('Book', back_populates='genre')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    status = Column(String, default="Unread")
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship('Genre', back_populates='books')

# Initialize the database
def initialize_database():
    """Set up the database and tables."""
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")

# Check Admin Rights
def check_admin():
    """Ensure the script is running with administrator privileges."""
    if os.name == 'nt':  # Windows
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("This script requires administrator privileges. Relaunching with elevated privileges...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            sys.exit()
    else:  # Unix/Linux
        if os.geteuid() != 0:
            print("This script requires administrator privileges. Please run with sudo.")
            sys.exit()

# Run in a New Terminal
def run_in_new_terminal():
    """Re-run the script in a new terminal window."""
    if os.name == 'nt':  # Windows
        if 'run_in_new_terminal' not in sys.argv:
            os.system(f'start cmd /k "{sys.executable} {__file__} run_in_new_terminal"')
            sys.exit()
    elif sys.platform == 'darwin':  # macOS
        if 'run_in_new_terminal' not in sys.argv:
            os.system(f'osascript -e \'tell application "Terminal" to do script "{sys.executable} {__file__} run_in_new_terminal"\'')
            sys.exit()
    else:  # Linux
        if 'run_in_new_terminal' not in sys.argv:
            os.system(f'gnome-terminal -- {sys.executable} {__file__} run_in_new_terminal')
            sys.exit()

# CLI Functions
def main_menu():
    print("=======================================")
    print("      Welcome to Book Manager CLI      ")
    print("=======================================")
    print("Select an option:")
    print("1. Add a Book")
    print("2. List All Books")
    print("3. Update Book Status")
    print("4. Delete a Book")
    print("5. Exit")

def add_book():
    session = Session()
    title = input("Enter the book title: ")
    author = input("Enter the author's name: ")
    genre_name = input("Enter the genre: ")

    genre = session.query(Genre).filter_by(name=genre_name).first()
    if not genre:
        genre = Genre(name=genre_name)
        session.add(genre)
        session.commit()

    new_book = Book(title=title, author=author, genre=genre, status="Unread")
    session.add(new_book)
    session.commit()
    print(f"Book '{title}' by {author} added successfully!")

def list_books():
    session = Session()
    books = session.query(Book).all()
    if not books:
        print("No books found in the collection.")
        return

    print("\nYour Book Collection:")
    for book in books:
        print(f"ID: {book.id} | Title: {book.title} | Author: {book.author} | Genre: {book.genre.name} | Status: {book.status}")

def update_book_status():
    session = Session()
    list_books()
    book_id = input("\nEnter the ID of the book you want to update: ")
    book = session.query(Book).get(book_id)

    if not book:
        print("Book not found.")
        return

    print(f"Current status of '{book.title}' is '{book.status}'.")
    new_status = input("Enter new status (Read/Unread): ").capitalize()

    if new_status in ["Read", "Unread"]:
        book.status = new_status
        session.commit()
        print(f"Status updated to '{new_status}' for '{book.title}'.")
    else:
        print("Invalid status. Please enter 'Read' or 'Unread'.")

def delete_book():
    session = Session()
    list_books()
    book_id = input("\nEnter the ID of the book you want to delete: ")
    book = session.query(Book).get(book_id)

    if not book:
        print("Book not found.")
        return

    session.delete(book)
    session.commit()
    print(f"Book '{book.title}' deleted successfully.")

def main():
    initialize_database()

    while True:
        main_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_book()
        elif choice == "2":
            list_books()
        elif choice == "3":
            update_book_status()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        check_admin()
        run_in_new_terminal()
    else:
        main()
