from core import ( BotDirectory, logger )

class TwitterBot(BotDirectory):
    """object to instantiate twitter bot for ritual"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__tweets: dict = {}
        self.__trends: dict = {}

    @property
    def tweets(self):
        return self.__tweets

    @property
    def trends(self):
        return self.__trends
        
    def getUserId(self, user: str) -> str:
        """function to get user id"""
        return self.client.get_user(user).id_str

    def getAvailableTrendLocations(self):
        """function to get all locations where trending information is available"""
        self.trendLocations: dict = self.client.trends_available()

    def getLocationTrends(self, woeid: int, name: str):
        """function to get trending hashtags for a given location"""
        self.trends[name]: list = self.client.trends_place(id=woeid)

    def searchPopularTweets(self, query: str):
        pass
        # search popular tweets to find seed material for 
        # the ai to generate from. 
        # Make a combination of the hashtags, and names to programmatically inject
        # this should happen in text after finding tweets
        

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