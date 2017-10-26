from .BaseModel import BaseModel
from peewee import CharField

class Email(BaseModel):

    email = CharField(max_length=50)
