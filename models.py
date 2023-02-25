from peewee import *
import datetime
from config import DBNAME, PWD
from playhouse.migrate import *


db = SqliteDatabase(f"{PWD}{DBNAME}")

class Equation(Model):
    equat            = CharField(unique=True)
    answer           = IntegerField(null=False)
    money            = IntegerField(null=False)
    
    class Meta:
        database = db

class Group(Model):
    # For stats and
    id               = PrimaryKeyField()
    tgid             = IntegerField(unique=True)
    add_dt           = DateTimeField(default=datetime.datetime.now)
    vaccine_start_dt = DateTimeField(null=True)
    is_vaccine       = BooleanField(default=False)
    vaccine          = BooleanField(default=False) 
    infected_users   = IntegerField(default=0)
    zero_infected    = IntegerField(null=True)
    treas            = IntegerField(default=0)

    class Meta:
        database = db  


class Price(Model):
    id               = PrimaryKeyField()
    injector         = IntegerField(default=10)
    vaccine          = IntegerField(default=990)
    cotton           = IntegerField(default=40)  # При покупке дается 5
    spirit           = IntegerField(default=200) # При покупке дается 150 мл

    class Meta:
        database = db  


class User(Model):
    id               = PrimaryKeyField()
    tgid             = IntegerField(null=False)
    group            = ForeignKeyField(Group, 'tgid')
    username         = CharField(null=True)
    full_name        = CharField(null=True)
    chances          = IntegerField(default=1)
    is_infected      = BooleanField(default=False)
    is_imune         = BooleanField(default=False)
    infected_usrs    = TextField(null=True) # join "+" and uses tgid
    infected_dt      = DateTimeField(null=True)
    cured_dt         = DateTimeField(null=True)
    job_dt           = DateTimeField(null=True)
    much_cured       = IntegerField(default=0)
    gen              = IntegerField(default=0)
    try_infect       = DateTimeField(null=True)
    money            = IntegerField(default=0)

    class Meta:
        database = db  

class Inventory(Model):
    id               = PrimaryKeyField()
    user             = ForeignKeyField(User, to_field='id')
    injector         = IntegerField(default=0) # Шприц
    spirit           = IntegerField(default=0) # Спирт
    cotton           = IntegerField(default=0) # Вата
    vaccine          = IntegerField(default=0) # Вакцина
    
    class Meta:
        database = db  


def my_migrate():
    migrator = SqliteMigrator(db)

    with db.atomic():
        migrate(
            migrator.add_column('Group', 'treas', IntegerField(default=0)),
        )


Price.create_table()
price, _ = Price.get_or_create(id=1)
if _:
    price.save()
del price, _
User.create_table()
Inventory.create_table()
Group.create_table()
Equation.create_table()

if __name__ == "__main__":
    my_migrate()