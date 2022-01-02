from core import (
    os, 
    pkl, 
    torch
)

SPECIAL_WORDS: dict = {'PADDING': '<PAD>'}

def load_data(path: str) -> str:

    text_file = os.path.join(path)
    with open(text_file, "r") as f:
        data = f.read()

    return data

def preprocess_and_save(
    text_path: str, 
    token_lookup: object, 
    creat_lookup_tables: object) -> None:

    text = load_data(path=text_path)
    token_dict = token_lookup()

    for key, token in token_dict.items():
        text = text.replace(key, f'{token}')

    text = text.lower()
    text = text.split()

    w2i, i2w = create_lookup_tables(text + list(SPECIAL_WORDS.values()))
    int_text = [w2i[word] for word in text]

    pkl.dump((int_text, w2i, i2w, token_dict), open('preprocess.p', 'wb'))

def load_preprocess():

    return pkl.load(open('preprocess.p', mode='rb'))







