# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
import json
import os


def get_user_list(config, key):
    with open(f"{os.getcwd()}/NekoRobot/{config}", "r") as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 13822678  # integer value, dont use ""
    API_HASH = "58307222e0ed42dc114fb9369511a100"
    TOKEN = "5797562455:AAFSPcySpTGc9IfULa85hk8XZo-l7_VxI0o"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 1109460378  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "chirag57"
    SUPPORT_CHAT = "peronaxsupport"  # Your own group for support, do not add the @
    JOIN_LOGGER = (
        -1001549961507
    )  # Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = (
        -1001549961507
    )  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    STRING_SESSION = ""
    # RECOMMENDED
    SQLALCHEMY_DATABASE_URI = "postgres://tluamgmb:wzHC-TipPrkuPGtbqHUpVNeGpqicuQCV@castor.db.elephantsql.com/tluamgmb"  # needed for any database modules
    DB_URL = "postgresql://postgres:IE2wA6q9yKhLpaqeJ0RT@containers-us-west-17.railway.app:5819/railway"
    REDIS_URL = ""
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = "P5_FWlwgUrpchwJceZDUSDxa41G396dn7J0vSEMWeBhHJ6C4q8VJLzjhfZPxNKUZ"  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"

    # OPTIONAL
    ##List of id's -  (not usernames) for users which have sudo access to the bot.
    DRAGONS = get_user_list("elevated_users.json", "sudos")
    ##List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = get_user_list("elevated_users.json", "supports")
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    WORKERS = (
        8  # Number of subthreads to use. Set as number of threads your processor uses
    )
    BAN_STICKER = ""  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = (
        "awoo"  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = "awoo"  # Get your API key from https://timezonedb.com/api
    WALL_API = (
        "awoo"  # For wallpapers, get one from https://wall.alphacoders.com/api.php
    )
    AI_API_KEY = "awoo"  # For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True  # Create a new config.py or rename this to config.py file in same dir and import, then extend this class.


import json
import os


def get_user_list(config, key):
    with open(f"{os.getcwd()}/NekoRobot/{config}", "r") as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 13822678  # integer value, dont use ""
    API_HASH = "58307222e0ed42dc114fb9369511a100"
    TOKEN = "5797562455:AAFSPcySpTGc9IfULa85hk8XZo-l7_VxI0o"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 1109460378  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "chirag57"
    SUPPORT_CHAT = "peronaxsupport"  # Your own group for support, do not add the @
    JOIN_LOGGER = (
        -1001549961507
    )  # Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = (
        -1001549961507
    )  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit

    # RECOMMENDED
    SQLALCHEMY_DATABASE_URI = "sqldbtype://username:pw@hostname:port/db_name"  # needed for any database modules
    DB_URL = "postgres://vwqvvwikvmvork:0e1c6c72408351d53079950a907fd45d87c7e0cb96d8f3c8aaf9818900e39f21@ec2-35-171-210-17.compute-1.amazonaws.com:5432/dbipmbeosdsfa9"
    REDIS_URL = ""
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = "P5_FWlwgUrpchwJceZDUSDxa41G396dn7J0vSEMWeBhHJ6C4q8VJLzjhfZPxNKUZ"  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"
    

    # OPTIONAL
    ##List of id's -  (not usernames) for users which have sudo access to the bot.
    DRAGONS = get_user_list("elevated_users.json", "sudos")
    ##List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = get_user_list("elevated_users.json", "supports")
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    WORKERS = (
        8  # Number of subthreads to use. Set as number of threads your processor uses
    )
    BAN_STICKER = ""  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = (
        "awoo"  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = "awoo"  # Get your API key from https://timezonedb.com/api
    WALL_API = (
        "awoo"  # For wallpapers, get one from https://wall.alphacoders.com/api.php
    )
    AI_API_KEY = "awoo"  # For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None
    STRING_SESSION =""
    ARQ_API_URL = "https://thearq.tech"
    ARQ_API_KEY = "KAWQFT-VKAEYR-AAMZCN-CKSEUZ-ARQ"
    BOT_USERNAME = "vanitas_tgbot"
    OPENWEATHERMAP_ID = ""
    REM_BG_API_KEY = ""
  


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
