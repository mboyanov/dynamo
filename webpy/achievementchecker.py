
from config import *
db = getDB()

class achievementchecker:
  def __init__(self):
    self.message=''
  
  def check(self,uid):
    count=db.query('Select count(*) as count from user_problems where id_user="'+str(uid)+'";')
    count=count[0]['count']
    print count
    if count==1:
      new = db.query("select * from user_achievements where user_id='"+str(uid)+"' AND achievement_id='1';")
      if len(new)==0:
	db.query('INSERT INTO user_achievements VALUES("'+str(uid)+'","1");')
	data=db.query("Select * from achievements where id='1';")
	data=data[0]
	self.message+='<br>Congratulations! You unlocked the '+data['title']+' achievement! <br> <img src="'+data['url']+'"> <br> Go to the <A href="/achievements">Achievements page </A> to generate your certificate!'
    elif count==3:
      new = db.query("select * from user_achievements where user_id='"+str(uid)+"' AND achievement_id='3';")
      if len(new)==0:
	db.query('INSERT INTO user_achievements VALUES("'+str(uid)+'","3");')
	data=db.query("Select * from achievements where id='3';")
	data=data[0]
	self.message+='<br>Congratulations! You unlocked the '+data['title']+' achievement! <br> <img src="'+data['url']+'"> <br> Go to the <A href="/achievements">Achievements page </A> to generate your certificate!'
    return self.message
  
