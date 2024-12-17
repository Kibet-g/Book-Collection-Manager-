from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Base class for declarative models
Base = declarative_base()

# Define the Genre model
class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship: A genre has many books
    books = relationship('Book', back_populates='genre')

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"

# Define the Book model
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    status = Column(String, default="Unread")  # 'Read' or 'Unread'

    # Foreign key and relationship with Genre
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship('Genre', back_populates='books')

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', status='{self.status}')>"

# Create database engine and session
DATABASE_URL = 'sqlite:///books.db'
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

def initialize_database():
    """Create tables in the database."""
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
