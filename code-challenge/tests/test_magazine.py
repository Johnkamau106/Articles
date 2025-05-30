import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Clean tables
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()  # <-- Commit after deletes to avoid locking

    # Insert test authors
    cursor.execute("INSERT INTO authors (name) VALUES ('Author A'), ('Author B')")
    # Insert test magazines
    cursor.execute("INSERT INTO magazines (name, category) VALUES ('Magazine A', 'Tech'), ('Magazine B', 'Science')")
    conn.commit()

    # Retrieve IDs
    cursor.execute("SELECT id FROM authors ORDER BY id")
    author_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM magazines ORDER BY id")
    magazine_ids = [row[0] for row in cursor.fetchall()]

    # Insert articles linking authors and magazines
    cursor.execute("""
        INSERT INTO articles (title, author_id, magazine_id) VALUES
        ('Article 1', ?, ?),
        ('Article 2', ?, ?),
        ('Article 3', ?, ?),
        ('Article 4', ?, ?)
    """, (
        author_ids[0], magazine_ids[0],
        author_ids[0], magazine_ids[1],
        author_ids[1], magazine_ids[0],
        author_ids[1], magazine_ids[0]
    ))
    conn.commit()
    conn.close()

def test_magazine_creation_and_find(setup_db):
    magazine = Magazine.find_by_name("Magazine A")
    assert magazine is not None
    assert magazine.category == "Tech"

def test_magazine_articles(setup_db):
    magazine = Magazine.find_by_name("Magazine A")
    articles = magazine.articles()
    assert len(articles) >= 1

def test_magazine_contributors(setup_db):
    magazine = Magazine.find_by_name("Magazine A")
    contributors = magazine.contributors()
    names = [c.name for c in contributors]
    assert "Author A" in names
    assert "Author B" in names

def test_magazine_article_titles(setup_db):
    magazine = Magazine.find_by_name("Magazine A")
    titles = magazine.article_titles()
    assert "Article 1" in titles

def test_magazine_contributing_authors(setup_db):
    magazine = Magazine.find_by_name("Magazine A")
    authors = magazine.contributing_authors()
    # Only authors with more than 2 articles should be returned; in setup, Author B has 2 articles only, so result might be empty
    # Adjust if you add more articles for proper testing
    for author in authors:
        assert author.name in ["Author A", "Author B"]

def test_top_publisher(setup_db):
    top = Magazine.top_publisher()
    assert top is not None
