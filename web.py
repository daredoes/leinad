from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.utils import download_file, create_tmp_file, database, till_white, till_end
import urllib
import urllib2
import re
import json, os

domain = "daredoes.work"


def good_response(key):
    return "This page can be reached at http://%s/%s" % (domain, key)


def web_new_link(key, url):
    try:
            urllib2.urlopen(url)
            attempt = urllib2.urlopen("https://%s/newLink?%s" % (domain, urllib.urlencode({"key": key, "link":url})))
            return True
    except:
        return False


m_link = "\\bmake link\\b %s (.*)" % till_white
@respond_to(m_link, re.IGNORECASE)
@listen_to(m_link, re.IGNORECASE)
def make_link(message, key, url):
    if message.is_approved('web'):
        url = url.strip('<> ')
        try:
            urllib2.urlopen(url)
            attempt = urllib2.urlopen("https://%s/newLink?%s" % (domain, urllib.urlencode({"key": key, "link":url})))
            message.send(attempt.read())
        except:
            message.send("Bad URL")
    else:
        message.send("User does not have sufficient permissions.")

g_link = "\\bgen link\\b (.*)"
@respond_to(g_link, re.IGNORECASE)
@listen_to(g_link, re.IGNORECASE)
def gen_link(message, url):
    if message.is_approved('web'):
        url = url.strip('<> ')
        try:
            urllib2.urlopen(url)
            attempt = urllib2.urlopen("http://%s/genLink?%s" % (domain, urllib.urlencode({"link":url})))
            message.send(attempt.read())
        except:
            message.send("Bad URL")
    else:
        message.send("User does not have sufficient permissions.")

master = "\\bmaster\\b"
@respond_to(master, re.IGNORECASE)
@listen_to(master, re.IGNORECASE)
def master_links(message):
    if message.is_approved('any'):
        try:
            attempt = urllib2.urlopen("http://%s/master" % (domain))
            message.upload_snippet(attempt.read().replace("<br>", "\n"), "Available Shortlinks")
        except:
            message.send("Unknown Error")
    else:
        message.send("User does not have sufficient permissions.")

b = "\\bbadges\\b"
@respond_to(b, re.IGNORECASE)
@listen_to(b, re.IGNORECASE)
def badges(message):
    if message.is_approved("any"):
        try:
            attempt = urllib2.urlopen("https://prime.uber.magfest.org/uber/registration/stats")
            thing = (attempt.read())
            info = json.loads(thing)
            message.send("Badges Sold: %s\n Badges Remaining: %s" % (info['badges_sold'], info['remaining_badges']))
        except KeyError:
            message.send("Bad URL")
