import json

from bson import json_util
from mongoengine import connect, Document, StringField, ListField, ReferenceField

connect(db="hw", host="mongodb://localhost:27017")

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)

# Читання даних з JSON-файлу
with open('authors.json') as f:
    authors_data = json.load(f)

with open('quotes.json') as f:
    quotes_data = json.load(f)

# Збереження даних в базі даних
for author_data in authors_data:
    author = Author(**author_data)
    author.save()

for quote_data in quotes_data:
    author = Author.objects(fullname=quote_data['author']).first()
    quote = Quote(author=author, **quote_data)
    quote.save()