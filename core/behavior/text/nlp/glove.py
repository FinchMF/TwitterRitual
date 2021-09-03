"""
Contains Glove to process and handle reading in glove vectors

author@matthewfinch
"""

from core import ( np, os, load_dotenv, logger )

class Glove:
    """object to read in glove vecors

       to initalize the object, input one of the following:
       glove-6B-50d
       glove-6B-100d
       glove-6B-200d
       glove-6B-300d

       glove-twitter-27B-25d
       glove-twitter-27B-50d
       glove-twitter-27B-100d
       glove-twitter-27B-200d
    """
    def __init__(self, vectors_file: str, verbose: bool = False):

        self.__embeddings: dict = {}
        self.__verbose: bool = verbose
        self.__vector_file: str = vector_file

    @property
    def embeddings(self) -> dict:
        return self.__embeddings

    @property
    def verbose(self) -> bool:
        return self.__verbose

    def intialize(self):
        """function to read in and set word emebddings"""
        try:
            _file = os.getenv(self.__vector_file)
            with open(_file, 'r') as v:
                for line in v:
                    data: list = line.split()
                    word: str = data[0]
                    vector: np.array = np.array(data[1:], dtype=np.float64)
                    self.embeddings[word]: np.array = vector
        except Exception as e:
            logger.info(f'Error | {e}')