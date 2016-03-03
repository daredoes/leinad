from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.utils import download_file, create_tmp_file, database, till_white, till_end
import re
import json, os
import random

db = database()

def memory_dict(term, thought):
    return {"key":term, "note":thought}

rem = "\\bremember\\b %s \\bis\\b %s" % (till_white, till_end)
@listen_to(rem, re.IGNORECASE)
@respond_to(rem, re.IGNORECASE)
def remember(message, key, note):
    if message.is_approved("any"):
        if db.mem.count({"key":key}) == 0:
            db.mem.insert_one(memory_dict(key, note))
            message.send("I'll be sure to remember that.")
        else:
            message.send("I already know something about %s" % key)

wha = "\\bwhat is\\b %s" % (till_white)
@listen_to(wha, re.IGNORECASE)
@respond_to(wha, re.IGNORECASE)
def what(message, key):
    if message.is_approved("any"):
        if db.mem.count({"key":key}) != 0:
            thing = db.mem.find({"key":key})
            for x in thing:
                message.send(x['note'])
        else:
            message.send("I don't know what %s is" % key)