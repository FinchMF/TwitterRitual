"""
Twitter Ritual -
SHORT DESCRIPTION:
    Twitter Ritual is an automated art process that takes place
    between four Twitter Bots. Each of these bots are owned by myself.
    Each bot has a role in the process and the art is a result of their
    automated interaction. The automation handles a degress of randomness.
    The automation includes a mixuture of AI generative content. 
"""
# built in imports
import os
import sys
import logging
# logger
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s - [ %(filename)s: %(lineno)d @ %(funcName)s ] - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
)
logger = logging.getLogger('Twitter-Ritual')
# libraries
from dotenv import load_dotenv
import tweepy
from tweepy import ( API, Cursor, OAuthHandler, TweepError, RateLimitError )
# modules
from core.twitterBot.credentials import Credentials
from core.twitterBot.botNames import BotDirectory
from core.twitterBot.twitterBot import TwitterBot


__author__ = 'Matthew Finch'
__maintainer__ = 'Matthew Finch'
__email__ = 'finchrmatthew@gmail.com'