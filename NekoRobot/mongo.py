import asyncio
import sys

from motor import motor_asyncio
from NekoRobot.__init__ import MONGO_DB_URI 
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from NekoRobot.conf import get_int_key, get_str_key
# from Shikimori.utils.logger import log


MONGO_PORT = get_int_key("27017")
MONGO_DB_URI = get_str_key("MONGO_DB_URI")
MONGO_DB = "Anya"


client = MongoClient()
client = MongoClient(MONGO_DB_URI, MONGO_PORT)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI, MONGO_PORT)
db = motor[MONGO_DB]
db = client["Anya"]
try:
  asyncio.get_event_loop().run_until_complete(motor.server_info())
except ServerSelectionTimeoutError:
  print("Can't connect to mongodb! Exiting...")
    # sys.exit(log.critical("Can't connect to mongodb! Exiting..."))
