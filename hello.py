from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.utils import download_file, create_tmp_file, database, till_white, till_end
import re
import json, os
import random

answer_key = ""
insults = [
    "Hey %s, you're dumb."
]

domain = "daredoes.work"
responses = []
db = database()

orders = {"66":"It shall be done, my liege.", "delta alfa romeo echo":"butts.",
          "overtaker": "Soon I will consume dragonbot whole."}

help_string = "who loves (term of love) - returns all users who love such a term\n" \
              "(this guy) loves (term of love) - adds a user to the list of lovers of (term of love)\n" \
              "approved users - returns a snippet of all users with permission in snakeman\n" \
              "execute order (order number) - returns a one-liner if one is worthy\n" \
              "start vote (write once for one vote per poll, write anything to be able to vote for multiple options) (key) (comma-seperated-options) - starts a global vote with the options given\n" \
              "vote (key) (option) - votes for the option on the poll with the given key\n" \
              "make link (key) (url) - generates a shortlink at magfe.st/(key) or magfest.rocks/(key)\n" \
              "gen link (url) - generates a random shortlink at magfe.st/(genKey) or magfest.rocks/(genKey)\n"


def command(regex, english_command, func, special=re.IGNORECASE, listen=True, respond=True, *args):
    if listen and not respond:
        @listen_to(regex, special)
        def bot_response(*args):
            func(*args)
    elif respond and not listen:
        @respond_to(regex, special)
        def bot_response(*args):
            func(*args)
    else:
        @listen_to(regex, special)
        @respond_to(regex, special)
        def bot_response(*args):
            func(*args)


def reply_to_tuple(trigger, response, perm):
    return (trigger, response, perm)


def random_ha():
    return str("ha" * random.randint(3,10))
orders['giggles'] = random_ha

def field_dict(title, value):
    return {"title": title, "value": value}


def user_dict(username, id, permissions=""):
    return {"user": username, "id": id, 'permissions': permissions}

def recur(trigger, response, perm):
    @listen_to(trigger, re.IGNORECASE)
    @respond_to(trigger, re.IGNORECASE)
    def basic_reply(message):
        if message.is_approved(perm):
            if isinstance(response, str):
                message.send(response)
            else:
                message.send(response())
        else:
            message.send("User does not have sufficient permissions.")

responses.append(reply_to_tuple("\\bbad\\b", "I'm sorry! Please forgive me!", "any"))
responses.append(reply_to_tuple("\\bbehave\\b", "I will do my *best*!", "any"))
responses.append(reply_to_tuple('\\blaugh\\b', random_ha, "any"))
responses.append(reply_to_tuple('\\bleave\\b', "You first!", "any"))
responses.append(reply_to_tuple('\\bpet\\b', "What a _kind_ gesture.", "any"))
responses.append(reply_to_tuple('\\bbite\\b', "*BITES BACK!*", "any"))
responses.append(reply_to_tuple('\\bactivate skynet\\b', "_Skynet_ *ACTIVATED*", "any"))
responses.append(reply_to_tuple('\\blove me\\b',"How about... *no.*", "any"))
responses.append(reply_to_tuple('\\b420\\b', "Drugs are *bad*. Stay in school.", "any"))

for x in responses:
    recur(x[0], x[1], x[2])


woagh = '\\bwo+?a+?g+?h+?\\b'
@listen_to(woagh, re.IGNORECASE)
@respond_to(woagh, re.IGNORECASE)
def woooaaagh(message):
    if message.is_approved("any"):
        message.react("trippy")
        message.send("*WOAAAAAAAGGHHHH!*\nhttps://pbs.twimg.com/media/B8JvTeMIIAAbXYA.jpg:large")

help_str = '\\bhelp\\b'
command_str= '\\bcommands\\b'
@listen_to(help_str, re.IGNORECASE)
@listen_to(command_str, re.IGNORECASE)
@respond_to(help_str, re.IGNORECASE)
@respond_to(command_str, re.IGNORECASE)
def help_commands(message):
    if message.is_approved("any"):
        message.upload_snippet(help_string, "Commands")


#command(a_users, "approved users - uploads a snippet of the users with snakeman permissions", approved)





test = "\\btest\\b"
@listen_to(test, re.IGNORECASE)
@respond_to(test, re.IGNORECASE)
def test(message):
    if message.is_approved("admin"):
        message.send(message.sent_by())



order_sent = "\\bexecute order\\b (.*$)"
@listen_to(order_sent, re.IGNORECASE)
@respond_to(order_sent, re.IGNORECASE)
def execute_orders(message, order):
    if message.is_approved("any"):
        if order in orders.keys():
            if isinstance(orders[order], str):
                message.send(orders[order])
            else:
                message.send(orders[order]())
    else:
        message.send("You are not worthy of executing such a command.")


