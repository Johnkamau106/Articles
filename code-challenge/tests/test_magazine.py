import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_database():
    """Fixture to set up the database before each test"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    
    # Create test data
    cursor.execute("INSERT INTO authors (name) VALUES ('Test Author 1'), ('Test Author 2')")
    cursor.execute("""
        INSERT INTO magazines (name, category) 
        VALUES ('Test Magazine 1', 'Tech'), 
               ('Test Magazine 2', 'Science')
    """)
    
    # Get the created IDs
    cursor.execute("SELECT id FROM authors ORDER BY id")
    author_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM magazines ORDER BY id")
    magazine_ids = [row[0] for row in cursor.fetchall()]
    
    # Create articles that link authors and magazines
    cursor.execute("""
        INSERT INTO articles (title, author_id, magazine_id)
        VALUES 
            ('Article 1', ?, ?),
            ('Article 2', ?, ?),
            ('Article 3', ?, ?),
            ('Article 4', ?, ?)
    """, (
        author_ids[0], magazine_ids[0],  # Author 1 in Magazine 1
        author_ids[0], magazine_ids[1],  # Author 1 in Magazine 2
        author_ids[1], magazine_ids[0],  # Author 2 in Magazine 1
        author_ids[1], magazine_ids[0]   # Author 2 in Magazine 1 (second article)
    ))
    
    conn.commit()
    conn.close()
    
    # Return the IDs for use in tests
    return {
        'author_ids': author_ids,
        'magazine_ids': magazine_ids
    }

def test_magazine_creation():
    """Test creating a new magazine"""
    magazine = Magazine.create("New Magazine", "Business")
    assert magazine.id is not None
    assert magazine.name == "New Magazine"
    assert magazine.category == "Business"
    
    # Verify it was saved to the database
    from_db = Magazine.find_by_id(magazine.id)
    assert from_db.name == magazine.name
    assert from_db.category == magazine.category

def test_find_by_id(setup_database):
    """Test finding a magazine by ID"""
    magazine = Magazine.find_by_id(setup_database['magazine_ids'][0])
    assert magazine is not None
    assert magazine.name == "Test Magazine 1"
    assert magazine.category == "Tech"

def test_find_by_name(setup_database):
    """Test finding a magazine by name"""
    magazine = Magazine.find_by_name("Test Magazine 2")
    assert magazine is not None
    assert magazine.id == setup_database['magazine_ids'][1]
    assert magazine.category == "Science"

def test_magazine_articles(setup_database):
    """Test retrieving articles for a magazine"""
    magazine = Magazine.find_by_id(setup_database['magazine_ids'][0])
    articles = magazine.articles()
    
    assert len(articles) == 3  # Should have 3 articles (2 from author 2, 1 from author 1)
    titles = [article.title for article in articles]
    assert "Article 1" in titles
    assert "Article 3" in titles
    assert "Article 4" in titles

def test_magazine_contributors(setup_database):
    """Test retrieving contributors to a magazine"""
    magazine = Magazine.find_by_id(setup_database['magazine_ids'][0])
    contributors = magazine.contributors()
    
    assert len(contributors) == 2  # Both authors have contributed
    names = [author.name for author in contributors]
    assert "Test Author 1" in names
    assert "Test Author 2" in names

def test_article_titles(setup_database):
    """Test retrieving article titles for a magazine"""
    magazine = Magazine.find_by_id(setup_database['magazine_ids'][0])
    titles = magazine.article_titles()
    
    assert len(titles) == 3
    assert "Article 1" in titles
    assert "Article 3" in titles
    assert "Article 4" in titles

def test_contributing_authors(setup_database):
    """Test finding authors with more than 2 articles in a magazine"""
    # First, add enough articles to make author 2 have 3 articles in magazine 1
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
        ("Extra Article", setup_database['author_ids'][1], setup_database['magazine_ids'][0])
    )
    conn.commit()
    conn.close()
    
    magazine = Magazine.find_by_id(setup_database['magazine_ids'][0])
    contributing_authors = magazine.contributing_authors()
    
    assert len(contributing_authors) == 1
    assert contributing_authors[0].name == "Test Author 2"

def test_top_publisher(setup_database):
    """Test finding the magazine with the most articles"""
    # Magazine 1 should have 3 articles, Magazine 2 has 1
    top_publisher = Magazine.top_publisher()
    assert top_publisher.id == setup_database['magazine_ids'][0]
    assert len(top_publisher.articles()) == 3

def test_magazine_update():
    """Test updating a magazine's attributes"""
    magazine = Magazine.create("Original Name", "Original Category")
    magazine.name = "Updated Name"
    magazine.category = "Updated Category"
    magazine.save()
    
    from_db = Magazine.find_by_id(magazine.id)
    assert from_db.name == "Updated Name"
    assert from_db.category == "Updated Category"

def test_magazine_delete(setup_database):
    """Test deleting a magazine"""
    magazine = Magazine.find_by_id(setup_database['magazine_ids'][0])
    magazine.delete()
    
    from_db = Magazine.find_by_id(setup_database['magazine_ids'][0])
    assert from_db is None
    
    # Verify articles were also deleted (due to ON DELETE CASCADE)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles WHERE magazine_id=?", (setup_database['magazine_ids'][0],))
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 0

def test_magazine_article_relationship(setup_database):
    """Test the relationship between magazines and articles"""
    magazine = Magazine.find_by_id(setup_database['magazine_ids'][0])
    articles = magazine.articles()
    
    for article in articles:
        assert article.magazine_id == magazine.id
        assert Article.find_by_id(article.id).magazine_id == magazine.id

def test_magazine_author_relationship(setup_database):
    """Test the relationship between magazines and authors through articles"""
    magazine = Magazine.find_by_id(setup_database['magazine_ids'][0])
    authors = magazine.contributors()
    
    # Verify each author has at least one article in this magazine
    for author in authors:
        author_articles = author.articles()
        assert any(article.magazine_id == magazine.id for article in author_articles)