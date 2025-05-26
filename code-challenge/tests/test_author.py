

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

    