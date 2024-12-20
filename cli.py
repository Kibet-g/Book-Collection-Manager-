#!/usr/bin/env python3

import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Base class for declarative models
Base = declarative_base()
engine = create_engine('sqlite:///books.db')  # Database file is books.db
Session = sessionmaker(bind=engine)


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

# Create the database and tables
def initialize_database():
    """Set up the database and tables."""
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")
# Main menu
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
# Add a new book to the collection
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
    main()
