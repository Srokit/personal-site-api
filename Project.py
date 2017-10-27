from peewee import CharField
from BaseModel import BaseModel

class Project(BaseModel):

    name = CharField(max_length=100, unique=True)
    description = CharField(max_length=300)
    logo_img_name = CharField(max_length=50)


    def to_dict(self):
        return {'name': self.name,
                'description': self.description,
                'logoImgName': self.logo_img_name}
