from config import *

db = getDB()


class achievementchecker:
    def __init__(self):
        self.message = ''

    def check(self, uid):
        count = db.query('Select count(*) as count from user_problems where id_user="' + str(uid) + '";')
        count = count[0]['count']
        if count == 1:
            new = db.query("select * from user_achievements where user_id='" + str(uid) + "' AND achievement_id='1';")
            if len(new) == 0:
                db.query('INSERT INTO user_achievements VALUES("' + str(uid) + '","1");')
                data = db.query("Select * from achievements where id='1';")
                data = data[0]
                self.message += '<br>Congratulations! You unlocked the ' + data['title'] + ' achievement! <br> <img src="' + \
                                data[
                                'url'] + '"> <br> Go to the <A href="/achievements">Achievements page </A> to generate your certificate!'
        elif count == 3:
            new = db.query("select * from user_achievements where user_id='" + str(uid) + "' AND achievement_id='3';")
            if len(new) == 0:
                db.query('INSERT INTO user_achievements VALUES("' + str(uid) + '","3");')
                data = db.query("Select * from achievements where id='3';")
                data = data[0]
                self.message += '<br>Congratulations! You unlocked the ' + data['title'] + ' achievement! <br> <img src="' + \
                                data[
                                    'url'] + '"> <br> Go to the <A href="/achievements">Achievements page </A> to generate your certificate!'
        elif count == 7:
            new = db.query("select * from user_achievements where user_id='" + str(uid) + "' AND achievement_id='5';")
            if len(new) == 0:
                db.query('INSERT INTO user_achievements VALUES("' + str(uid) + '","5");')
                data = db.query("Select * from achievements where id='5';")
                data = data[0]
                self.message += '<br>Congratulations! You unlocked the ' + data['title'] + ' achievement! <br> <img src="' + \
                                data[
                                    'url'] + '"> <br> Go to the <A href="/achievements">Achievements page </A> to generate your certificate!'
        elif count == 10:
            new = db.query("select * from user_achievements where user_id='" + str(uid) + "' AND achievement_id='6';")
            if len(new) == 0:
                db.query('INSERT INTO user_achievements VALUES("' + str(uid) + '","6");')
                data = db.query("Select * from achievements where id='6';")
                data = data[0]
                self.message += '<br>Congratulations! You unlocked the ' + data['title'] + ' achievement! <br> <img src="' + \
                                data[
                                    'url'] + '"> <br> Go to the <A href="/achievements">Achievements page </A> to generate your certificate!'

        return self.message

    def awardSurvey(self, uid):
        data = db.query("Select * from achievements where type='survey'")
        data = data[0]
        db.query("replace into user_achievements VALUES({0},{1})".format(uid, data['id']))
        self.message += '<br>Congratulations! You unlocked the ' + data['title'] + ' achievement! <br> <img src="' + \
                        data[
                            'url'] + '"> <br> Go to the <A href="/achievements">Achievements page </A> to generate your certificate!'
        return self.message