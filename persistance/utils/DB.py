from peewee import *
from peewee_extra_fields import *
import datetime
from .. import models
db = SqliteDatabase('data.db')



def Seed():
    if  models.User.select().count() == 0:
        
        user = models.User(
            username='Admin', 
            password='123', 
            active=True, 
            api_token='123123123',
            token_recycled_date=datetime.datetime.now(),
            activated_date=datetime.datetime.now(),
        )
        
        print('creating the admin user..', user.save())
    else:
        print('Skipping seeding...')