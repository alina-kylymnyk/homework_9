from mongoengine import connect
import json
from mongoengine.errors import NotUniqueError
from models import Author, Quote  

# Підключення до локальної MongoDB
connect(
    db='your_database_name',  
    host='localhost',        
    port=27017,              
    username='host',  
    password='host'   
)

if __name__ == '__main__':
    # Збереження авторів
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(
                    name=el.get('name'),
                    birthdate=el.get('birthdate'),
                    bio=el.get('bio')
                )
                author.save()
            except NotUniqueError:
                print(f"Автор вже існує {el.get('name')}")

    # Збереження цитат
    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            author = Author.objects(name=el.get('author')).first()
            if author is not None:
                quote = Quote(
                    text=el.get('text'),
                    tags=el.get('tags'),
                    author=author
                )
                quote.save()
            else:
                print(f"Автор не знайдено для цитати: {el.get('text')}")
