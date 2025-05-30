
# lib/debug.py
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

def start_console():
    print("Starting interactive console...")
    print("Available objects:")
    print("- Author: Author model class")
    print("- Magazine: Magazine model class")
    print("- Article: Article model class")
    print("- seed_database(): Function to seed the database")
    
    # Start interactive console
    import code
    code.interact(local=locals())

if __name__ == '__main__':
    start_console()
    