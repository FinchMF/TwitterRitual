
from core import ( TwitterBot, Glitcher, random, os )

class Cycle(TwitterBot, Glitcher):
    """object to initiate a bot and it's twitter ritual"""
    __actor: list = ['INITIATOR', 'RESPONDER', 'INTERPRETER', 'MANIPULATOR']

    def __init__(self):
        
        self.__randomActorIdx: int = random.randint(0, len(Cycle.__actor)-1)
        self.__actor: str = os.getenv(Cycle.__actor[self.__randomActorIdx])
        self.__role: str = Cycle.__actor[self.__randomActorIdx]
        TwitterBot.__init__(self, bot=self.role)
        Glitcher.__init__(self)

    @property
    def actor(self) -> str:
        return self.__actor

    @property
    def role(self) -> str:
        return self.__role

    def ritual(self):

        # invoke actions to make edits
        # make materials (images for now) - later text
        # interaction cycle 
        # 
        # check to see is any bots have left messages
        # check trends
        # generate text
        # glitch image
        # post link 
        # post glitched image
        # post generated text
        # 
        # figure out what trends behavior can be made 
        pass

    def allComment(
        self, 
        text: str = None, 
        image: str = None, 
        in_reply_to: str = None) -> dict:

        success: dict = {}
        bots = [ role for role in list(self.botConnections.keys()) if role != self.role ]
        self.postTweet(text=text, image=image, in_reply_to=in_reply_to)
        success[self.actor] = True

        for bot in bots:

            try:
                TwitterBot.__init__(self, bot=bot)

                if in_reply_to is None:
                    self.postTweet(
                        text=text, 
                        image=image)
                else:
                    self.postTweet(
                        text=text,
                        image=image, 
                        in_reply_to=in_reply_to
                    )
                success[bot] = True
            except Exception as e:
                print(e)
                success[bot] = False

        return success