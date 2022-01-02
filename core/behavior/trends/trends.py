"""
Contains process for Trends to be searched

author@matthewfinch
"""
from core import ( random, datetime )

class Trend(object):

    def __init__(self, TwitterBot: object):

        self.__bot: object = TwitterBot
        self.__memory: list = []
    
    @property
    def bot(self) -> object:
        return self.__bot

    @property
    def memory(self) -> list:
        return self.__memory


    def _random_topic(self, location_name: str) -> dict:

        """function to validate location"""

        try: 
            topic: dict = random.choice(
                self.bot.trends[location_name][0]['trends']
            )
            topic['response']: str = 'Success'
        
        except Exception as e:

            topic: dict = {
                'reponse': 'ERROR',
                'Error': e
            }

        return topic


    def addRandomLocationTopics(self) -> None:

        """function to add a random location's trends and set location to memory"""

        # get full list of available locations      
        self.bot.getAvailableTrendLocations()
        # get random location
        random_location: dict = random.choice(self.bot.trendLocations)
        # get random topics from random location
        self.bot.getLocationTrends(woeid=random_location['woeid'],
                                   name=random_location['name'])
        # set location and search criteria to memory
        self.memory.append(
            {'name': random_location['name'], 'woeid': random_location['woeid']}
        )

    def searchTopic(self, random_location: bool = True, 
                          location: dict = None, 
                          records: int = 10, 
                          date = datetime.datetime.now().strftime("%Y-%m-%d")) -> list:

        """function to find random trend from a location
            location can be random if none is specified"""

        if random_location:

            if len(self.memory) == 0:
                self.addRandomLocationTopics()

            location: dict = random.choice(self.memory)
    
        random_topic: dict = self._random_topic(location_name=location['name'])

        if random_topic['response'] == 'ERROR':

            self.bot.getLocationTrends(woied=location['woied'], name=location['name'])
            random_topic: dict = self._random_topic(location_name=location['name'])

        self.bot.searchPopularTweets(query=random_topic['name'], records=records, date=date)
        # if there was going to be a filter class ;)
        data = [ tweet._json for tweet in self.bot.trendTweets[random_topic['name']] ]

        return data


    def getAllQuery(self) -> list:
        """returns a list of all topics
            - should this be a property?"""
        pass