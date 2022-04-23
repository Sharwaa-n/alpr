from web.utils import config
config.realize_env()


from web.app import application
from persistance import initDb, models
from datetime import date


initDb()

# user = models.User(username='Yameen', password='123', active=True, api_token='34234234', token_recycled_date=date(1960, 1, 15), activated_date=date(1960, 1, 15))
# user.save()
# models.DetectionRequest(image='someimage', user_id=1, ip='::1').save()





if __name__ == '__main__':
    print(application.url_map)
    application.run(debug=True,)

# from persistance import initDb, User


# user = User()
# charlie = User.create(username='charlie')
# huey = User(username='huey')
# huey.save()


# print(User().select().get().tweets.get())