# lib/db/seed.py
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    
    # Create sample authors
    authors = [
        Author("John Doe"),
        Author("Jane Smith"),
        Author("Bob Johnson")
    ]
    for author in authors:
        author.save()
    
    # Create sample magazines
    magazines = [
        Magazine("Tech Today", "Technology"),
        Magazine("Science Weekly", "Science"),
        Magazine("Business Insights", "Business")
    ]
    for magazine in magazines:
        magazine.save()
    
    # Create sample articles
    articles = [
        Article("The Future of AI", authors[0].id, magazines[0].id),
        Article("Quantum Computing Breakthrough", authors[1].id, magazines[1].id),
        Article("Market Trends 2023", authors[2].id, magazines[2].id),
        Article("Python for Data Science", authors[0].id, magazines[0].id),
        Article("Renewable Energy Advances", authors[1].id, magazines[1].id)
    ]
    for article in articles:
        article.save()
    
    conn.close()
    print("Database seeded successfully!")
    