"""
Contains Trainer for model and data
Trainer can store the corpus, model and trained embeddings

author@matthewfinch
"""

from core import ( Word2vec, TEXT )

class Model:
    """object to train model"""
    # currently the only model it is training is Word2vec
    def __init__(self, corpus: str, epochs: int = 2000):

        self.corpus: str = corpus
        self.NN: object = Word2vec()
        self.epochs: int = epochs

    def processText(self):
        """function to process text"""
        # self.corpus: str = TEXT.format(corpus=self.corpus)
        self.corpus: list = TEXT.preprocess(corpus=self.corpus)

    def prepare(self):
        """function to prepare text and model"""
        TEXT.prepareData(corpus=self.corpus, model=self.model)

    def train(self):
        """train model"""
        self.NN.train(epochs=self.epochs)

    def save(self, model_name: str) -> object:
        """function to save model"""
        with open(f"models/{model_name}_{self.epochs}.pkl", 'rb') as m:
            pickle.dump(self.NN, m)