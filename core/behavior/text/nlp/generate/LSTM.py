from core import nn

class LSTM(nn.Module):

    def __init__(self, 
                 vocab_size: int,
                 output_size: int,
                 embedding_dim: int,
                 hidden_dim: int,
                 n_layers: int,
                 dropout: float = 0.5):

        super(LSTM, self).__init__()

        self.vocab_size: int = vocab_siz
        self.output_size: int = output_size
        self.embedding_dim: int = embedding_dim
        self.hidden_dim: int = hidden_dim
        self.n_layers: int = n_layers
        self.dropout: float = dropout

        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, n_layers, dropout=dropout, batch_first=True)
        self.dropout = nn.Dropout(dropout)

        self.fcl = nn.Linear(hidden_dim, output_size)
        self.sig = nn.Sigmoid()

    def forward(self, nn_input, hidden):

        pass


    def init_hidden(self, batch_size):

        pass


