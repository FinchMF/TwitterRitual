
from core import ( TwitterBot, Glitcher, random, os )

class Cycle(TwitterBot, Glitcher):
    """object to initiate a bot and it's twitter ritual"""
    __actor: list = ['INITIATOR', 'RESPONDER', 'INTERPRETER', 'MANIPULATOR']

    def __init__(self):
        
        self.__randomActorIdx: int = random.randint(0, len(Cycle.__actor)-1)
        self.__actor: str = os.getenv(Cycle.__actor[self.__randomActorIdx])
        TwitterBot.__init__(self, bot=self.actor)
        Glitcher.__init__(self)

    @property
    def actor(self) -> str:
        return self.__actor

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