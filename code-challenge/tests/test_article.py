import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Clean tables
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()  # <-- Added commit here to avoid locking

    # Setup sample data
    author = Author("Test Author")
    author.save()
    magazine = Magazine("Test Magazine", "Test Category")
    magazine.save()
    article = Article("Test Article", author.id, magazine.id)
    article.save()

    yield

    conn.close()

def test_article_creation(setup_db):
    articles = Article.find_by_title("Test Article")
    assert len(articles) == 1
    article = articles[0]
    assert article.title == "Test Article"

def test_article_relationships(setup_db):
    article = Article.find_by_title("Test Article")[0]
    author = article.author()
    magazine = article.magazine()

    assert author.name == "Test Author"
    assert magazine.name == "Test Magazine"

def test_find_by_author(setup_db):
    author = Author.find_by_name("Test Author")
    articles = Article.find_by_author(author.id)
    assert any(a.title == "Test Article" for a in articles)

def test_find_by_magazine(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    articles = Article.find_by_magazine(magazine.id)
    assert any(a.title == "Test Article" for a in articles)

def test_article_save_update(setup_db):
    article = Article.find_by_title("Test Article")[0]
    article.title = "Updated Title"
    article.save()

    updated = Article.find_by_id(article.id)
    assert updated.title == "Updated Title"

def test_article_delete(setup_db):
    article = Article.find_by_title("Test Article")[0]
    article.delete()

    deleted = Article.find_by_id(article.id)
    assert deleted is None
