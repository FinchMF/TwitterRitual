from core import ( Credentials, BotDirectory, logger )

class TwitterBot(Credentials):
    """object to instantiate twitter bot for ritual"""
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.client = self.getClient()
        self.connections = BotDirectory().botConnections
        self.tweets: dict = {}

    def getUserId(self, user: str) -> str:
        """function to get user id"""
        return self.client.get_user(user).id_str

    def recieveTweet(self, user: str, most_recent: bool = False):
        """function to recieve tweets from user"""
        userId = self.getUserId(user=user)
        if most_recent:
            tweets = self.client.user_timeline(id=userId, count=1)[0]
        else:
            tweets = self.client.user_timeline(id=userId)
        
        self.tweets[user] = tweets

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

    