import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()

    # Create test data
    author = Author("Test Author")
    author.save()
    magazine = Magazine("Test Magazine", "Test")
    magazine.save()
    article = Article("Test Article", author.id, magazine.id)
    article.save()
    
    yield
    conn.close()

def test_author_save_and_find(setup_db):
    author = Author.find_by_name("Test Author")
    assert author is not None
    assert author.name == "Test Author"

def test_author_articles(setup_db):
    author = Author.find_by_name("Test Author")
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "Test Article"

def test_author_magazines(setup_db):
    author = Author.find_by_name("Test Author")
    magazines = author.magazines()
    assert len(magazines) == 1
    assert magazines[0].name == "Test Magazine"

def test_author_add_article(setup_db):
    author = Author.find_by_name("Test Author")
    magazine = Magazine.find_by_name("Test Magazine")
    new_article = author.add_article(magazine, "New Article")
    assert new_article.title == "New Article"
    assert len(author.articles()) == 2