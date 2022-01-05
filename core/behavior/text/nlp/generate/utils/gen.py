import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F 

def generate(
    model: object,
    prime_id: int,
    i2w: dict,
    token_dict: dict,
    pad_value: int,
    sequence_length: int,
    predict_len: int = 100
) -> str:

    model.eval()

    curr_seq: np.array = np.full((1, sequence_length), pad_value)
    curr_seq[-1][-1] = prime_id
    pred = [i2w[prime_id]]

    for _ in range(predicted_len):

        if train_on_gpu:
            curr_seq = torch.LongTensor(curr_seq).cuda()
        
        else:
            curr_seq = torch.LongTensor(curr_seq)

        
        hidden = model.init_hidden(curr_seq.size(0))
        output, _ = model(curr_seq, hidden)
        p = F.softmax(output, dim=1).data

        if train_on_gpu:
            p = p.cpu()

        top_k: int = 5
        p, top_idx = p.topk(top_k)
        top_idx = top_idx.numpy().squeeze()

        p = p.numpy().squeeze()
        word_idx = np.random.choice(top_idx, p=p/p.sum())

        word = i2w[word_idx]
        pred.append(word)

        curr_seq = np.roll(curr_seq, -1, 1)
        curr_seq[-1][-1] = word_idx

    gen_sentences = ' '.join(pred)

    for word, token in token_dict.items():

        ending = ' ' if word in ['\n', '(', '"'] else ''
        gen_sentences = gen_sentences.replace(' ' + token.lower(), word)

    gen_sentences = gen_sentences.replace('\n ', '\n')
    gen_sentences = gen_sentences.replace('( ', '(')

    return gen_sentences

        
