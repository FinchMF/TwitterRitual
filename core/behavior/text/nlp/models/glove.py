"""
Contains Glove to process and handle reading in glove vectors

author@matthewfinch
"""

from core import ( np, sys )

class Glove:
    """object to read in glove vecors"""
    def __init__(self, vectors_file: str, verbose: bool = False):

        self.__embeddings: dict = {}
        self.__verbose: bool = verbose

    @property
    def embeddings(self) -> dict:
        return self.__embeddings

    @property
    def verbose(self) -> bool:
        return self.__verbose

    def intialize(self):
        """function to read in and set word emebddings"""
        with open(vectors_file, 'r') as v:
            for line in v:
                data: list = line.split()
                word: str = data[0]
                vector: np.array = np.array(data[1:], dtype=np.float64)
                self.embeddings[word]: np.array = vector