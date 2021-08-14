from core import ( Credentials, load_dotenv, os )

class BotDirectory(Credentials):
    """object containing handles by ritual role"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__bots: dict = {
            'INITIATOR': os.getenv('INITIATOR'),
            'RESPONDER': os.getenv('RESPONDER'),
            'INTERPRETER': os.getenv('INTERPRETER'),
            'MANIPULATOR': os.getenv('MANIPULATOR')
        }
        
        self.getClient()
        self.genConnections()

    @property
    def bots(self):
        return self.__bots

    @property
    def botConnections(self):
        return self.__botConnections

    def genConnections(self):
        """ function to generate the handles each bot can communicate with"""
        self.__botConnections: dict = {role: [name for name in self.bots.values() if name != self.bots[role]] for role in self.bots.keys()}