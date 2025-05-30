# lib/controllers/article_controller.py
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.article import Article

def add_author_with_articles(author_name, articles_data):
    """
    Adds an author and their articles in a single transaction
    articles_data: List of dictionaries with 'title' and 'magazine_id' keys
    Returns the created Author object if successful, None otherwise
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Begin transaction
        conn.execute("BEGIN")
        
        # Insert author
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
        author_id = cursor.lastrowid
        
        # Insert articles
        for article in articles_data:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (article['title'], author_id, article['magazine_id'])
            )
        
        # Commit transaction
        conn.commit()
        
        # Return the new author
        return Author.find_by_id(author_id)
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Transaction failed: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()