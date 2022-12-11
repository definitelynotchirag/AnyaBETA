import codecs
import pickle

from typing import Dict, List , Union

from NekoRobot.mongo import db

dalcdb = db.dalc 

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


async def get_dalcs(user_id: int) -> Dict[str, int]:
    dalc = dalcdb.find_one({"user_id": user_id})
    if not dalc:
        return {}
    return dalc["dalc"]

async def update_dalc(user_id:int, dalc: dict):
    # name = name.lower().strip()
    dalcs = await get_dalcs(user_id)
    dalcs[dalc] = dalc
    dalcdb.update_one({"$set": {"dalc": dalc}}, upsert=True)


# async def get_dalc(name: str) -> Union[bool, dict]:
#     name = name.lower().strip()
#     dalcs = await get_dalcs(user_id)
#     if name in dalcs:
#         return name

