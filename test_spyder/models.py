from mongoengine import Document, fields

class Author(Document):
    name = fields.StringField()
    birthdate = fields.StringField()
    bio = fields.StringField()

class Quote(Document):
    text = fields.StringField()
    author = fields.ReferenceField(Author)
    tags = fields.ListField(fields.StringField())
