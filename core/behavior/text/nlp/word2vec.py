"""
Contains Word2vec model 

author@matthewfinch
"""

from core import ( np, softmax, logger )

class Word2vec(object):
    """object to generate word vectors
       word2vec skip gram"""
    def __init__(self):

        self.N: int = 10 # number neurons in the hidden layer
        self.X_train: list = []
        self.y_train: list = []
        self.window_size: int = 2
        self.lr: float = 0.001
        self.words: list = []
        self.word_index: dict = {}
   
    def initialize(self, V: int, data: list):
        """function to intiailize model"""
        self.V: int = V
        self.W: list = np.random.uniform(-0.8, 0.8, (self.V, self.N))
        self.W1: list = np.random.uniform(-0.8, 0.8, (self.N, self.V))
        self.words: list = data
        for i in range(len(data)):
            self.word_index[data[i]]: int = i
   

    def feed_forward(self, X: list) -> float:
        """funciton to pass forward through the model"""
        self.h: list = np.dot(self.W.T,X).reshape(self.N,1)
        self.u: list = np.dot(self.W1.T,self.h)
        #print(self.u)
        self.y: float = softmax(self.u)  
        return self.y
           
    def backpropagate(self, x: list, t: list):
        """function to backpropograte through the model"""
        e: list = self.y - np.asarray(t).reshape(self.V,1)
        # e.shape is V x 1
        dLdW1: list = np.dot(self.h,e.T)
        X: list = np.array(x).reshape(self.V,1)
        dLdW: list = np.dot(X, np.dot(self.W1,e).T)
        self.W1: list = self.W1 - self.lr*dLdW1
        self.W: list = self.W - self.lr*dLdW
           
    def train(self, epochs: int):
        """function to train model"""
        for x in range(1, epochs):        
            self.loss: int = 0
            for j in range(len(self.X_train)):
                self.feed_forward(self.X_train[j])
                self.backpropagate(self.X_train[j],self.y_train[j])
                C: int = 0
                for m in range(self.V):
                    if(self.y_train[j][m]):
                        self.loss += -1*self.u[m][0]
                        C += 1
                self.loss += C*np.log(np.sum(np.exp(self.u)))
            logger.info(f" | EPOCH {x} | loss = {self.loss}")
            self.lr *= 1/( (1+self.lr*x) )
              
    def predict(self,word: str, number_of_predictions: int):
        """function to predict word context"""
        if word in self.words:
            index: int = self.word_index[word]
            X: list = [0 for i in range(self.V)]
            X[index]: int = 1
            prediction: float = self.feed_forward(X)
            output: dict = {}
            for i in range(self.V):
                output[prediction[i][0]]: int = i
               
            top_context_words: int = []
            for k in sorted(output,reverse=True):
                top_context_words.append(self.words[output[k]])
                if(len(top_context_words)>=number_of_predictions):
                    break
       
            return top_context_words
        else:
            print("Word not found in dicitonary")