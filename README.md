Book Collection Manager
Overview
The Book Collection Manager is a simple Command Line Interface (CLI) application for managing a collection of books. Built using Python and SQLAlchemy ORM, it allows users to add, view, update, and delete books from a database. The project demonstrates the integration of a relational database with Python, following best practices for CLI and ORM applications.

Features
Add new books with their title, author, and genre.
List all books with their details.
Update the reading status of a book (Read or Unread).
Delete books from the collection.
Automatically initialize the database on first run.
Uses SQLAlchemy ORM for database operations.
Project Structure
bash
Copy code
Book-Collection-Manager/
├── models.py          # Defines the database schema and ORM models
├── main.py            # Main entry point for the CLI application
├── Pipfile            # Dependency and virtual environment manager
├── Pipfile.lock       # Locked dependency versions
└── README.md          # Documentation
Prerequisites
Ensure you have the following installed on your system:

Python 3.10 or later
Pipenv (for managing dependencies)
Setup Instructions
Clone the Repository

bash
Copy code
git clone <repository-url>
cd Book-Collection-Manager
Set Up the Virtual Environment

bash
Copy code
pipenv install
Activate the Virtual Environment

bash
Copy code
pipenv shell
Initialize the Database
Run the models.py script to create the database and tables:

bash
Copy code
python models.py
How to Run the Project
Start the CLI Application
Run the main script to launch the CLI:

bash
Copy code
python main.py
Using the CLI
Follow the on-screen menu to interact with the application:

Add a new book by entering its title, author, and genre.
View all books in your collection.
Update the status of a book (e.g., mark as "Read").
Delete books from the collection.
Technologies Used
Python: Primary programming language for the application.
SQLAlchemy ORM: For database schema definition and interaction.
SQLite: Lightweight database for storing book records.
Future Enhancements
Add support for advanced filtering and sorting.
Implement Alembic for managing database migrations.
Expand the schema to include additional features like Authors or Loan History.
Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request with your improvements or suggestions.

License
This project is licensed under the MIT License.