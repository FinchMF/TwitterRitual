from core import ( load_env, os )

class BotDirectory:
    """object containing handles by ritual role"""
    def __init__(self):
        self.bots: dict = {
            'INITIATOR': os.getenv('INITIATOR'),
            'RESPONDER': os.getenv('RESPONDER'),
            'INTERPRETER': os.getenv('INTERPRETER'),
            'MANIPULATOR': os.getenv('MANIPULATOR')
        }
        self.genConnections()
    def genConnections(self):
        """ function to generate the handles each bot can communicate with"""
        self.botConnections: dict = {role: [name for name in self.bots.values() if name != self.bots[role]] for role in self.bots.keys()}