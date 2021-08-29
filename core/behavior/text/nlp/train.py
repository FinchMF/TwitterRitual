"""
Contains Trainer for model and data
Trainer can store the corpus, model and trained embeddings

author@matthewfinch
"""

from core import ( word2vec, TEXT )

class Trainer:
    """object to train model"""
    # currently the only model it is training is Word2vec
    def __init__(self, corpus: str, epochs: int = 2000):

        self.corpus: str = corpus
        self.model: object = Word2vec()
        self.epochs: int = epochs

    def processText(self):
        """function to process text"""
        self.corpus: str = TEXT.format(corpus=self.corpus)
        self.corpus: list = TEXT.preprocess(corpus=self.corpus)

    def prepare(self):
        """function to prepare text and model"""
        TEXT.prepareData(corpus=self.corpus, model=self.model)

    def train(self):
        """train model"""
        self.model.train(epochs=self.epochs)