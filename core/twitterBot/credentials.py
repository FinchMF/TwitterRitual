from core import ( OAuthHandler, API, os, load_dotenv )

class CredentialError(Exception):
    pass

class Credentials:
    """object to handle fetching appropiate bot API keys and authentification"""
    def __init__(self, bot: str):

        self.__bot: str = bot
        self.fetch()
        self.authenticate()
    
    @property
    def bot(self):
        return self.__bot

    @property
    def creds(self):
        return self.__creds

    def fetch(self):
        """function to fetch appropiate API keys"""
        self.__creds: dict = {
            'consumer_key': os.getenv(f'{self.bot}_CONSUMER'),
            'consumer_secret_key': os.getenv(f'{self.bot}_CONSUMER_SECRET'),
            'access_token': os.getenv(f'{self.bot}_ACCESS'),
            'access_secret_token': os.getenv(f'{self.bot}_ACCESS_SECRET')
        }
    def authenticate(self):
        """function to authenticate keys"""
        try:
            self.auth: object = OAuthHandler(self.creds['consumer_key'], self.creds['consumer_secret_key'])
            self.auth.set_access_token(self.creds['access_token'], self.creds['access_secret_token'])
        except Exception as e:
            raise CredentialError(f'Credentials for {self.bot} did not authenticate | check environment | error on {e}')

    def getClient(self):
        """function to connect client"""
        self.client = API(self.auth)