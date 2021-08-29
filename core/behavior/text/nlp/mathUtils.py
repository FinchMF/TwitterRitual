from core import ( np )

def softmax(x: float) -> float:
    """Compute softmax values for each sets of scores in x."""
    e_x: float = np.exp(x - np.max(x))
    return e_x / e_x.sum()