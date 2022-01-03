# from core import (
#     os, 
#     pkl, 
#     torch
# )
import os
import pickle as pkl
import torch
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

def load_preprocess(text_title: str = None):

    return pkl.load(open(f'processedData/{text_title}_preprocess.p', mode='rb'))

def convertManyToOne(texts: list) -> str:

    text: str = ''
    for txt in texts:

        text += load_data(txt)

    return text



