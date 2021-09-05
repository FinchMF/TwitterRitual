"""
Contains image glitch operations pipeline

author@matthewfinch
"""

from core import ( os, random, load_dotenv, Glitch, glob )

class Glitcher(Glitch):
    """object to randomize parameters and choose random image
       from AI generated images"""
    def __init__(self, image_directory: str = 'CLARITY_frames'):

        self.__image_directory: str = image_directory
        self.__parameters: dict = {'pathIn': None,
                                   'pathOut': None,
                                   'amnt': None,
                                   'seed': None,
                                   'n_iter': None,
                                   'verbose': True}
        self.initRandomParameters()

    @property
    def image_directory(self) -> str:
        return self.__image_directory

    @property
    def parameters(self) -> dict:
        return self.__parameters

    def initRandomParameters(self):
        """function to generate random parameters for glitch"""
        images: list = glob(f"{os.getenv('unprocessed_images')}{self.image_directory}/*")
        rand_img_idx: int = random.randint(0, len(images)-1)

        self.parameters['pathIn']: str = images[rand_img_idx]
        self.parameters['pathOut']: str = f"{os.getenv('processed_images')}glitched_{rand_img_idx}.jpg"
        self.parameters['amnt']: float = random.random()
        self.parameters['seed']: float = random.random()
        self.parameters['n_iter']: int = random.randint(0, 60)
        super().__init__(**self.parameters)