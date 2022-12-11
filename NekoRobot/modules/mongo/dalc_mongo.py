from NekoRobot.mongo import db


dalc_statusdb = db.dalc_status

def is_dalc(user_id):
  dalc = dalc_statusdb.find_one({"user_id" : user_id})
  if not dalc:
    return False
  else :
    return True

def set_dalc(user_id):
  dalc = is_dalc(user_id)
  if dalc :
    return
  else :
    return dalc_statusdb.insert_one({"user_id":user_id})


def rem_dalc(user_id):
  dalc = is_dalc(user_id)
  if not dalc:
    return

  else :
    return dalc_statusdb.delete_one({"user_id":user_id})

