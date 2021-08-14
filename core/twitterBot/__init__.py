
"""
Twitter Ritual
"""
import os
import sys
import logging

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s - [ %(filename)s: %(lineno)d @ %(funcName)s ] - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
)
logger = logging.getLogger('Twitter-Ritual')

from dotenv import load_dotenv
import tweepy
from tweepy import ( API, Cursor, OAuthHandler, TweepError, RateLimitError )

from core.twitterBot.credentials import Credentials
from core.twitterBot.botNames import BotDirectory


__author__ = 'Matthew Finch'
__maintainer__ = 'Matthew Finch'
__email__ = 'finchrmatthew@gmail.com'