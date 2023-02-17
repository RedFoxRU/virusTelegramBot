from peewee import *
import datetime
from config import DBNAME, PWD


db = SqliteDatabase(f"{PWD}{DBNAME}")



class QuestProgress(Model):
    pass



class User(Model):
    tgid          = IntegerField(null=False, unique=True)
    username      = CharField()
    full_name     = CharField()
    chances       = IntegerField(default=1)
    is_infected   = BooleanField()
    infected_usrs = TextField() # join "+" and uses tgid
    infected_dt   = DateTimeField(default=datetime.datetime.now)
    cured_dt      = DateTimeField(default=datetime.datetime.now)
    much_cured    = IntegerField(default=0)
    gen           = IntegerField(default=0)
    try_infect    = DateField(default=datetime.datetime.now)
    

    class Meta:
        database = db  

class Group(Model):
    # For stats and 
    
    tgid           = IntegerField(unique=True)
    add_dt         = DateTimeField(default=datetime.datetime.now)
    infected_users = IntegerField(default=0)
    zero_infected  = IntegerField(null=True)

    class Meta:
        database = db  


User.create_table()
Group.create_table()