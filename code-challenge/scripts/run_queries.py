#!/usr/bin/env python3
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

def print_header(title):
    print("\n" + "="*50)
    print(f"=== {title.upper()}")
    print("="*50)

def run_queries():
    # First, seed the database with sample data
    seed_database()
    
    # 1. Basic queries
    print_header("basic queries")
    
    # Get all authors
    authors = [
        Author.find_by_name("John Doe"),
        Author.find_by_name("Jane Smith"),
        Author.find_by_name("Bob Johnson")
    ]
    
    print("Authors in system:")
    for author in authors:
        print(f"- {author.name} (ID: {author.id})")
    
    # Get all magazines
    magazines = [
        Magazine.find_by_name("Tech Today"),
        Magazine.find_by_name("Science Weekly"),
        Magazine.find_by_name("Business Insights")
    ]
    
    print("\nMagazines in system:")
    for magazine in magazines:
        print(f"- {magazine.name} (Category: {magazine.category}, ID: {magazine.id})")
    
    # 2. Relationship queries
    print_header("relationship queries")
    
    # Get all articles by John Doe
    john = Author.find_by_name("John Doe")
    print(f"\nArticles by {john.name}:")
    for article in john.articles():
        magazine = Magazine.find_by_id(article.magazine_id)
        print(f"- '{article.title}' in {magazine.name}")
    
    # Get all magazines John has written for
    print(f"\nMagazines {john.name} has contributed to:")
    for magazine in john.magazines():
        print(f"- {magazine.name} ({magazine.category})")
    
    # 3. Magazine queries
    tech_today = Magazine.find_by_name("Tech Today")
    print(f"\nArticles in {tech_today.name}:")
    for article in tech_today.articles():
        author = Author.find_by_id(article.author_id)
        print(f"- '{article.title}' by {author.name}")
    
    # 4. Complex queries
    print_header("complex queries")
    
    # Find magazines with articles by at least 2 different authors
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, COUNT(DISTINCT a.author_id) as author_count
        FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
        HAVING author_count >= 2
    """)
    print("\nMagazines with articles by at least 2 authors:")
    for row in cursor.fetchall():
        magazine = Magazine(row['name'], row['category'], row['id'])
        print(f"- {magazine.name} ({row['author_count']} authors)")
    conn.close()
    
    # Count the number of articles in each magazine
    print("\nArticle count by magazine:")
    for magazine in magazines:
        print(f"- {magazine.name}: {len(magazine.articles())} articles")
    
    # Find the author who has written the most articles
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*, COUNT(ar.id) as article_count
        FROM authors a
        LEFT JOIN articles ar ON a.id = ar.author_id
        GROUP BY a.id
        ORDER BY article_count DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    top_author = Author(row['name'], row['id'])
    print(f"\nTop author: {top_author.name} with {row['article_count']} articles")
    conn.close()
    
    # 5. Magazine methods
    print_header("magazine methods")
    
    science_weekly = Magazine.find_by_name("Science Weekly")
    print(f"\nArticle titles in {science_weekly.name}:")
    for title in science_weekly.article_titles():
        print(f"- {title}")
    
    print(f"\nContributing authors to {science_weekly.name}:")
    for author in science_weekly.contributors():
        print(f"- {author.name}")
    
    # 6. Transaction example
    print_header("transaction example")
    
    from lib.controllers.article_controller import add_author_with_articles
    
    new_articles = [
        {"title": "New Article 1", "magazine_id": tech_today.id},
        {"title": "New Article 2", "magazine_id": science_weekly.id}
    ]
    
    new_author = add_author_with_articles("New Author", new_articles)
    if new_author:
        print(f"\nSuccessfully added author {new_author.name} with articles:")
        for article in new_author.articles():
            magazine = Magazine.find_by_id(article.magazine_id)
            print(f"- '{article.title}' in {magazine.name}")
    else:
        print("\nFailed to add author with articles")
    
    # 7. Bonus queries
    print_header("bonus queries")
    
    # Magazine.top_publisher()
    top_publisher = Magazine.top_publisher()
    print(f"\nMagazine with most articles: {top_publisher.name} with {len(top_publisher.articles())} articles")
    
    # Author topic areas
    print("\nAuthor topic areas:")
    for author in authors:
        print(f"{author.name} writes about: {', '.join(author.topic_areas())}")
    
    # Magazine.contributing_authors()
    print(f"\nAuthors with more than 2 articles in {tech_today.name}:")
    for author in tech_today.contributing_authors():
        print(f"- {author.name}")

if __name__ == '__main__':
    run_queries()