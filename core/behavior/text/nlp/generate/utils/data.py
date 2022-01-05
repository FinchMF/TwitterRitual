
import os
import pickle as pkl
import torch
from torch.utils.data import TensorData, DataLoader
import numpy as np
from collections import Counter


SPECIAL_WORDS: dict = {'PADDING': '<PAD>'}

def load_data(path: str) -> str:

    text_file = os.path.join(path)
    with open(text_file, "r") as f:
        data = f.read()

    return data

def token_lookup():
    return {
        '.': '||period||',
        ',': '||comma||',
        '"': '||quotation_mark||',
        ';': '||semicolon||',
        '!': '||exclamation_mark||',
        '?': '||question_mark||',
        '(': '||left_parentheses||',
        ')': '||right_Parentheses||',
        '-': '||dash||',
        '\n': '||return||'
    }

def create_lookup_tables(text: str) -> tuple:

    word_counts = Counter(text)
    sorted_vocab = sorted(word_counts, key=word_counts.get, reverse=True)
    i2w = {idx: word for idx, word, in enumerate(sorted_vocab)}
    w2i = {word: idx for idx, word in i2w.items()}

    return (w2i, i2w)

def preprocess_and_save(
    
    text_path: str,
    text_title: str, 
    token_lookup: object = token_lookup, 
    create_lookup_tables: object = create_lookup_tables) -> None:

    text = load_data(path=text_path)
    token_dict = token_lookup()

    for key, token in token_dict.items():
        text = text.replace(key, f'{token}')

    text = text.lower()
    text = text.split()

    w2i, i2w = create_lookup_tables(text + list(SPECIAL_WORDS.values()))
    int_text = [w2i[word] for word in text]

    pkl.dump((int_text, w2i, i2w, token_dict), open(f'processedData/{text_title}_preprocess.p', 'wb'))

def load_preprocess(text_title: str = None) -> tuple:
    """
        returns:
            int_text
            w2i
            i2w
            token_dict
            
    """
    return pkl.load(open(f'processedData/{text_title}_preprocess.p', mode='rb'))

def convertManyToOne(texts: list) -> str:

    text: str = ''
    for txt in texts:

        text += load_data(txt)

    return text

def batch_data(
    words: list,
    squence_lenght: int,
    batch_size: int) -> DataLoader:

    words: np.array = np.array(words)
    total_batch_size: int = batch_size * sequence_length
    n_batches: int = len(words) // batch_size

    words: np.array = words[:n_batches * total_batch_size]
    feature: list = []
    target: list = []

    target_len: np.array = words[:-sequence_length]

    for idx in range(0, len(target_len)):

        feature.append(words[idx: idx + sequence_length])
        target.append(words[idx + sequence_length])

    batch_nums: int = len(words) // batch_size
    batch_dim: int = batch_nums * batch_size

    feature = feature[:batch_dim]
    target = target[:batch_dim]
    feature = torch.from_numpy(np.asarray(feature))
    target = torch.from_numpy(np.asarray(target))

    data = TensorDataset(feature, target)
    data = DataLoader(data, batch_size=batch_size, shuffle=True)

    return data



def save_model(filename: str, decoder: object) -> None:

    #s_filename = os.path.splitext(os.path.basename(filename))[0] + '.pt'
    torch.save(decoder, filename)

def load_model(filename: str) -> object:

    #s_filename = os.path.spiltext(os.path.basename(filename))[0] + '.pt'
    return torch.load(filename)