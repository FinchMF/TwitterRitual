"""
Contains Vocab and TEXT to process corpus and embedd text to model
FUTURE: 
    - add in analysis such as tfidf
    - add method to compare embedding statistics
    - add in methods to add ngrams
    - add in methods to generate POS tagging

Corpus can be a single text or speech or multiples

author@matthefinch         
"""
# NOTE: do these methods help with generative text?
# NOTE: update format function
from core import ( punctuation, stopwords )

class VocabError(Exception):
    pass

class Vocab:
    """object to build vocabulary"""
    def __init__(self, corpus: list):

        self.__corpus: list = corpus
        self.__wordCount: dict = {}
        self.__length: int = None
        self.__words: dict = {}

    @property
    def corpus(self) -> list:
        return self.__corpus

    @corpus.setter
    def corpus(self, corpus: list):
        if isinstance(corpus, list):
            self.__corpus: list = corpus
        else:
            raise VocabError(f'Vocab.corpus only supports type list\
                             | type {type(corpus)} was passed')
        
    @property
    def wordCount(self) -> dict:
        return self.__wordCount

    @wordCount.setter
    def wordCount(self, wordCount: dict):
        if isinstance(wordCount, dict):
            self.__wordCount: dict = wordCount
        else:
            raise VocabError(f'Vocab.wordCount only supports type dict\
                              | type {type(wordCount)} was passed')
        
    @property
    def length(self) -> int:
        return self.__length

    @length.setter
    def length(self, length: int):
        if isinstance(length, int):
            self.__length: int = length
        else:
            VocabError(f'Vocab.length only supports type int\
                        | type {type(length)} was passed')

    @property
    def words(self) -> dict:
        return self.__words

    @words.setter
    def words(self, words: dict):
        if isinstance(words, dict):
            self.__words: dict = words
        else:
            VocabError(f'Vocab.words only supports dict\
                        | type {type(words)} was passed')


    def build(self):
        """build vocab"""
        words: dict = {}
        for sentence in self.corpus:
            for word in sentence:
                if word not in words:
                    words[word] = 1
                else:
                    words[word] += 1
        
        self.length: int = len(words)
        self.wordCount: dict = words
        self.data: list = sorted(list(words.keys()))
        
        for i in range(len(words)):
            self.words[self.data[i]] = i


class TEXT:
    """object to handle vocab and text processing"""
    @staticmethod
    def format(corpus: str) -> str:
        # format speech and text to necessary state for preprocessing 
        pass

    @staticmethod
    def preprocess(corpus: str) -> list:
        """function to process corpus"""
        stopWords: list = list(set(stopwords.words('english')))
        processedCorpus: list = []
        sentences: list = corpus.split('.') # double check how text / corpus is formatted
        for i in range(len(sentences)):
            sentences[i]: str = sentences[i].strip()
            sentence: list = sentences[i].split()
            sentence: list = [word.strip(punctuation) for word in sentence 
                                            if word not in stopWords]
            sentence: list = [word.lower() for word in sentence]
            processedCorpus.append(sentence)

        return processedCorpus

    @staticmethod
    def prepareData(corpus: list, model: object) ->  tuple:
        """function to prepare data to train model using skip gram"""

        VOCAB: object = Vocab(corpus=corpus)
        VOCAB.build()

        for sentence in corpus:
            for i in range(len(sentence)):
                centerWord: list = [0 for x in range(VOCAB.length)]
                centerWord[VOCAB.words[sentence[i]]]: int = 1
                context: list = [0 for x in range(VOCAB.length)]

                for j in range(i-model.window_size, i+model.window_size):
                    if i!=j and j>=0 and j<len(sentence):
                        context[VOCAB.words[sentence[j]]] += 1
                model.X_train.append(centerWord)
                model.y_train.append(context)
        model.initialize(VOCAB.length, VOCAB.data)

        return model.X_train, model.y_train