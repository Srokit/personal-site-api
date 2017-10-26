from peewee import CharField
from BaseModel import BaseModel

class Project(BaseModel):

    name = CharField(max_length=100)
    description = CharField(max_length=300)

    def to_dict(self):
        return {'name': self.name,
            'description': self.description}
