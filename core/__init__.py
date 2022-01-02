#!/usr/bin/python
"""
Twitter Ritual -
SHORT DESCRIPTION:
    Twitter Ritual is an automated art process that takes place
    between four Twitter Bots. Each of these bots are owned by myself.
    Each bot has a role in the process and the art is a result of their
    automated interaction. The automation handles degrees of randomness.
    The automation includes a mixuture of AI generative content and rule based
    manipulation. 
"""
# built in imports
import io
import os
import re
import sys
import copy
import random
import logging
import requests
import random
import datetime
import pickle as pkl
from glob import glob
from string import punctuation
# logger
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s - [ %(filename)s: %(lineno)d @ %(funcName)s ] - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
)
logger = logging.getLogger('Twitter-Ritual')
# libraries
from bs4 import BeautifulSoup
from PIL import Image
from dotenv import load_dotenv
import numpy as np
import nltk
from nltk.corpus import stopwords
import torch
import torch.nn as nn
import tweepy
from tweepy import ( API, Cursor, OAuthHandler, TweepError, RateLimitError )
# modules
from core.twitterBot.credentials import Credentials
from core.twitterBot.botNames import BotDirectory
from core.twitterBot.twitterBot import TwitterBot
from core.behavior.image.glitch import Glitch
from core.behavior.image.glitcher import Glitcher
from core.behavior.text.webscraper.baudrillard.URLS import URLS as BaudrillardURLS
from core.behavior.text.webscraper.politicians.URLS import URLS as PoliticianURLS
from core.behavior.text.webscraper.crawler import ( BaudrillardCrawler, PoliticianCrawler )
from core.behavior.text.nlp.mathUtils import softmax
from core.behavior.text.nlp.word2vec import Word2vec
from core.behavior.text.nlp.preprocess import TEXT
from core.behavior.text.nlp.model import Model
from core.behavior.text.nlp.glove import Glove
from core.behavior.trends.trends import Trend
from core.ritual.cycle import Cycle


__author__ = 'Matthew Finch'
__maintainer__ = 'Matthew Finch'
__email__ = 'finchrmatthew@gmail.com'
