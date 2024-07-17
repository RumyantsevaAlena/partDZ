import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['books_toscrape_com']
collection = db['books']

with open('books.json', 'r', encoding='utf-8') as f:
   books_data = json.load(f)

collection.insert_many(books_data)

# первая запись
print(collection.find()[0])

# количество документов в коллекции
print(collection.count_documents({}))

# фильтрация документов по критериям
query = {'category': 'Travel'}
print(collection.count_documents(query))

# Использование проекции
query = {'category': 'Travel'}
projection = {"_id": 0, "name": 1, "price": 1, "available": 1}
for rec in collection.find(query, projection):
   print(rec)

# Использование оператора $lt и $gte
MIN = 2
MAX = 20
query = {"available": {"$lt": MIN}}
print(f"Книги в наличии меньше {MIN}: {collection.count_documents(query)}")
query = {"available": {"$gte": MAX}}
print(f"Книги в наличии не меньше {MAX}: {collection.count_documents(query)}")

# Использование оператора $regex
WORD = "Moon"
query = {"name": {"$regex": WORD, "$options": "i"}}
print(f"Количество книг, в названии которых есть слово '{WORD}': {collection.count_documents(query)}")

# Использование оператора $in
query = {"category": {"$in": ["Travel", "Romance", "Classic"]}}
print(f'кол-во книг в категориях путешествий, романтика или классика :{collection.count_documents(query)}')

# Использование оператора $all
query = {"category": {"$all": ["Mystery"]}}
print(f'кол-во всех мистических книг :{collection.count_documents(query)}')

# Использование оператора $ne
query = {"category" : {"$ne": "Mystery"}}
print(f'кол-во книг кроме мистических :{collection.count_documents(query)}')
