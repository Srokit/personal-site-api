
from peewee import Model
import config
from playhouse.db_url import connect

db = connect(config.DB_URL)

class BaseModel(Model):
    class Meta:
        database = db
