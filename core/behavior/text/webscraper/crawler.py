from core import ( requests, BeautifulSoup, URLS )


class Crawler:
    textRoot = './core/behavior/text/webscraper/baudrillard/'
    """object to scrape baudrillard"""
    def __init__(self):

        self.__text: dict = {}

    @property
    def text(self):
        return self.__text

    def chooseText(self, title: str):
        """function to choose endpoint"""
        self.title: str = title
        self.endpoint: str = URLS.simulations if title == 'simulations' else URLS.simulationAndSimulacra

    def scrapeText(self):
        """function to collect text"""
        res: object = requests.get(self.endpoint)
        page: object = BeautifulSoup(res.content, 'html.parser')
        self.text[self.title]: str = page.find(id='maincontent').find('pre').text

    def saveText(self):
        """funciton to save text"""
        with open(f'{Crawler.textRoot}{self.title}.txt', 'w') as f:
            f.write(self.text[self.title])