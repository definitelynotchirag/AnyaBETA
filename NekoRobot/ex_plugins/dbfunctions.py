import codecs
import pickle
from typing import Dict, List , Union

from NekoRobot.mongo import db

karmadb = db.karma

async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        index = alphabet.index(i)
        user_id += str(index)
    user_id = int(user_id)
    return user_id

async def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text

async def get_karmas_count() -> dict:
    chats = karmadb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return {}
    chats_count = 0
    karmas_count = 0
    for chat in await chats.to_list(length=1000000):
        for i in chat["karma"]:
            karma_ = chat["karma"][i]["karma"]
            if karma_ > 0:
                karmas_count += karma_
        chats_count += 1
    return {"chats_count": chats_count, "karmas_count": karmas_count}

# async def get_karmas(chat_id: int) -> Dict[str, int]:
    # karma = karmadb.find_one({"chat_id": chat_id})
    # if not karma:
    #     return {}
    # return karma["karma"]

# async def get_karma(chat_id: int, name: str) -> Union[bool, dict]:
async def get_karma(name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    # karmas = await get_karmas(chat_id)
    # if name in karmas:
    return name


# async def update_karma(chat_id: int, name: str, karma: dict):
async def update_karma(name: str, karma: dict):
    name = name.lower().strip()
    # karmas = await get_karmas(chat_id)
    # karmas[name] = karma
    karmadb.update_one({"$set": {"karma": karma}}, upsert=True
    )

async def is_karma_on(chat_id: int) -> bool:
    chat = karmadb.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False

async def karma_on(chat_id: int):
    is_karma = is_karma_on(chat_id)
    if is_karma:
        return
    return karmadb.delete_one({"chat_id": chat_id})

async def karma_off(chat_id: int):
    is_karma = is_karma_on(chat_id)
    if not is_karma:
        return
    return karmadb.insert_one({"chat_id": chat_id})