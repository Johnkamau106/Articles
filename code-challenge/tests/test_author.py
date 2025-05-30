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
    conn.commit()  # <-- Commit after delete

    # Setup test data
    author = Author("Author One")
    author.save()
    magazine = Magazine("Magazine One", "Category One")
    magazine.save()
    article = Article("Article One", author.id, magazine.id)
    article.save()

    yield

    conn.close()

def test_author_creation_and_find(setup_db):
    author = Author.find_by_name("Author One")
    assert author is not None
    assert author.name == "Author One"

def test_author_articles(setup_db):
    author = Author.find_by_name("Author One")
    articles = author.articles()
    assert any(a.title == "Article One" for a in articles)

def test_author_magazines(setup_db):
    author = Author.find_by_name("Author One")
    magazines = author.magazines()
    assert any(m.name == "Magazine One" for m in magazines)

def test_author_add_article(setup_db):
    author = Author.find_by_name("Author One")
    magazine = Magazine.find_by_name("Magazine One")
    article = author.add_article(magazine, "New Article")
    assert article.id is not None
    assert article.title == "New Article"

def test_author_topic_areas(setup_db):
    author = Author.find_by_name("Author One")
    topics = author.topic_areas()
    assert "Category One" in topics
