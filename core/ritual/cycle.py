
from core import ( TwitterBot, Glicher, random, os )

class Cycle(TwitterBot, Glitcher):
    """object to initiate a bot and it's twitter ritual"""
    __actor: list = ['INITIATOR', 'RESPONDER', 'INTERPRETER', 'MANIPULATOR']

    def __init__(self):
        
        self.__randomActorIdx: int = random.randint(0, len(Cycle.__actor)-1)
        self.__actor: str = os.getenv(Cycle.__actor[self.__randomActorIdx])

    @property
    def actor(self) -> str:
        return self.__actor
    
    @property
    def bot(self) -> TwitterBot:
        return self.__bot

    @property
    def G(self) -> Glitcher:
        return self.__G

    def initBot(self):
        """function to initialize bot"""
        self.__bot: TwitterBot = super(TwitterBot, self).__init__(bot=self.actor)

    def initGlitch(self):
        """function to initialize glitch functionality"""
        self.__G: Glitcher = super(Glitcher, self).__init__()

    def ritual(self):

        # invoke actions to make edits
        # make materials (images for now) - later text
        # interaction cycle  
        pass