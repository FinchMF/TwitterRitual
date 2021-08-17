from core import ( BotDirectory, Cursor, logger )

class TwitterBot(BotDirectory):
    """object to instantiate twitter bot for ritual"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__tweets: dict = {}
        self.__trends: dict = {}
        self.__trendTweets: dict = {}

    @property
    def tweets(self):
        return self.__tweets

    @property
    def trends(self):
        return self.__trends

    @property
    def trendTweets(self):
        return self.__trendTweets
        
    def getUserId(self, user: str) -> str:
        """function to get user id"""
        return self.client.get_user(user).id_str

    def getAvailableTrendLocations(self):
        """function to get all locations where trending information is available"""
        self.trendLocations: dict = self.client.trends_available()

    def getLocationTrends(self, woeid: int, name: str):
        """function to get trending hashtags for a given location"""
        self.trends[name]: list = self.client.trends_place(id=woeid)

    def searchPopularTweets(self, query: str, records: int, date: str):
        """function to search tweets by query and date:
                - used to find tweets from trending hashtags and names"""
        tweets: list = []
        count: int = 0
        if self.verbose: logger.info(f'Calling Twitter | {date} | {search_query}') # check searching locations?

        for page in Cursor(self.client.seach,
                           q=query, lang='en',
                           since=date, tweet_mode='extended',
                           wait_on_rate_limit=True, count=200).pages(records):
            for tweet in page:
                tweets.append(tweet) # maybe build a filter here?

        if self.verbose: logger.info(f"PAGE: {count} | Tweets Filtered: {len(tweets)}")
        count += 1

        self.trendTweets[query]: list = tweets
        
    def readTweet(self, user: str, most_recent: bool = False):
        """function to recieve tweets from user"""
        userId = self.getUserId(user=user)
        if verbose: logger.info(f'{self.bot} is engaging with {user}')
        if most_recent:
            tweets: list = self.client.user_timeline(id=userId, count=1)
        else:
            tweets: list = self.client.user_timeline(id=userId)
        try:
            self.tweets[user].extend(tweets)
        except:
            self.tweets[user]: list = tweets

    def retweet(self, tweet_id: str):
        """function to retweet"""
        self.client.retweet(id=tweet_id)

    def postTweet(self, text: str = None, image: str = None, verbose: bool = False, in_reply_to: str = None):
        """function to tweet"""
        if text and image:
            self.client.update_with_media(filename=image, status=text, in_reply_to_status_id=in_reply_to)
            if verbose: logger.info(f"{self.bot} tweeted - TEXT: {text} | IMAGE: {image}")

        elif image and text == None:
            self.client.update_with_media(filename=image, in_reply_to_status_id=in_reply_to)
            if verbose: logger.info(f"{self.bot} tweeted - IMAGE: {image}")
        
        else:
            self.client.update_status(status=text, in_reply_to_status_id=in_reply_to)
            if verbose: logger.info(f"{self.bot} tweeted - TEXT: {text}")