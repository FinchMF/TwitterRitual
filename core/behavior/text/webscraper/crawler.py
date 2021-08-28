"""
Contains text crawlers to generate training and seed data
for TwitterBot text behaviors during the Twitter Ritual

author@matthewfinch
"""

from core import ( requests, BeautifulSoup, 
                   BaudrillardURLS, PoliticianURLS,
                   os, logger, re )

class ScraperError(Exception):
    pass

class BaudrillardCrawler:
    """crawler to collect Baudrillard text"""
    # location for baudrillard text
    textRoot = './core/behavior/text/webscraper/baudrillard/textData/'
    """object to scrape baudrillard"""
    def __init__(self, verbose: bool = False):

        self.__text: dict = {}
        self.__verbose: bool = verbose

    @property
    def text(self):
        return self.__text

    @property
    def verbose(self):
        return self.__verbose

    def chooseText(self, title: str):
        """function to choose endpoint"""
        self.title: str = title
        if title == 'simulations':
            self.endpoint: str = BaudrillardURLS.simulations 
            if self.verbose: logger.info(f'Scrapping Endpoint: {self.endpoint}')
        elif title == 'simulacra-and-simulations':
            self.endpoint: str = BaudrillardURLS.simulationAndSimulacra
            if self.verbose: logger.info(f'Scrapping Endpoint: {self.endpoint}')
        else:
            raise ScraperError(f'Title: {title} not supported.\
            Please choose from: "simulations" | "simulacra-and-simulations"')

    def scrapeText(self):
        """function to collect text"""
        res: object = requests.get(self.endpoint)
        page: object = BeautifulSoup(res.content, 'html.parser')
        self.text[self.title]: str = page.find(id='maincontent').find('pre').text
        if self.verbose: logger.info(f'{self.title} scrapped and stored')

    def saveText(self):
        """funciton to save text"""
        _file: str = f'{BaudrillardCrawler.textRoot}{self.title}.txt' 
        with open( _file, 'w') as f:
            f.write(self.text[self.title])
        if self.verbose: logger.info(f'Saved at: {_file}')


class PoliticianCrawler:
    """crawler to collect all presidental speeches"""
    # location for politcal text
    textRoot = './core/behavior/text/webscraper/politicians/textData/'
    def __init__(self, verbose: bool = False):

        self.__verbose: bool = verbose

    @property
    def verbose(self):
        return self.__verbose

    def saveSpeeches(self, speech_links: list):
        """function to save speeches"""
        for link in speech_links:
            # build url
            url: str = PoliticianURLS.root+''.join(link)
            # grab speech title [date:title-of-speech]
            title: str = url.split('/')[-1]
            #print(title)
            res: object = requests.get(url)
            page: object = BeautifulSoup(res.content, 'html.parser')
            # capture text
            text: list = []
            for i in page.find_all('p'):
                text.append(i.get_text())
            # set name and date of speech
            pres_name: str = '-'.join(''.join(text[1:2]).replace('.', '').split(' ')).lower()
            dos: str = '-'.join(''.join(text[2:3]).replace(',', '').split(' ')).lower()

            if self.verbose: logger.info(f'Speech on Date: {dos} given by {pres_name}')
            # save speech in a folder per president [pres-name/date-title.txt]
            try:
                os.mkdir(f'{PoliticianCrawler.textRoot}{pres_name}')
                if self.verbose: logger.info(f'Directory Made: {pres_name}')
            except FileExistsError:
                # create and write file
                _file: str = f'{PoliticianCrawler.textRoot}{pres_name}/{title}.txt'
                with open( _file, 'w') as f:
                    # write only the speech text
                    for t in text[3:-2]:
                        f.write(f'{t}\n')

    def fetchSpeeches(self):
        """function to fetch all presidental speeches"""
        # capture all speech links
        speech_links: list = []
        for page in range(0, PoliticianURLS.pages):
            # set url
            url: str = PoliticianURLS.speeches_page
            page_url: str = PoliticianURLS.page_url
            if self.verbose: logger.info(f'Page {page} Gathered...')
            speeches: str = f'{url}{page_url}{page}'
            res: object = requests.get(speeches)
            page: object = BeautifulSoup(res.content, 'html.parser')
            # capture speech links per page
            links: str = []
            for link in page.find_all('a', href=True):
                if re.match('/the-presidency/presidential-speeches/', link['href']):
                    links.append(link['href'])
                    
            speech_links.extend(links)
        # pass all speech links to function that scrapes speech text from link
        self.saveSpeeches(speech_links=speech_links)