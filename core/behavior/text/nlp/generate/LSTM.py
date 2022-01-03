"""
Contains LSTM architecture for text generator 
"""


import torch
import torch.nn as nn

class LSTM(nn.Module):

    def __init__(self, 
                 vocab_size: int,
                 output_size: int,
                 embedding_dim: int,
                 hidden_dim: int,
                 n_layers: int,
                 dropout: float = 0.5):

        super(LSTM, self).__init__()

        self.vocab_size: int = vocab_size
        self.output_size: int = output_size
        self.embedding_dim: int = embedding_dim
        self.hidden_dim: int = hidden_dim
        self.n_layers: int = n_layers
        self.dropout: float = dropout

        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, n_layers, dropout=dropout, batch_first=True)
        self.dropout = nn.Dropout(dropout)

        self.fcl = nn.Linear(hidden_dim, output_size)
        self.sig = nn.Sigmoid()

        self.train_on_gpu = True if torch.cuda.is_available() else False

    def forward(self, nn_input, hidden):

        batch_size = nn_input.size(0)
        nn_input = nn_input.long()

        embedded_output = self.embeddings(nn_input)
        lstm_output, hidden = self.lstm(embedded_output)

        lstm_output = self.dropout(lstm_output)
        lstm_output = self.fcl(lstm_output)
        lstm_output = self.sig(lstm_output)

        lstm_output = lstm_output.view(batch_size, -1, self.output_size)

        output = lstm_output[:, -1]

        return output, hidden


    def init_hidden(self, batch_size):

        weight = next(self.parameters()).data

        W = weight.new(self.n_layers, batch_size, self.hidden_dim).zero_()

        if self.train_on_gpu:

            hidden = ( W.cuda(), W.cuda())

        else:

            hidden =  (W, W)


        return hidden