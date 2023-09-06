import torch
from torch import nn
import torch.nn.functional as F

import numpy as np
import pandas as pd

def one_hot_encoder(encoded_text, num_uni_chars):
    '''
    encoded_text : batch of encoded text
    
    num_uni_chars = number of unique characters (len(set(text)))

    METHOD FROM:
        https://stackoverflow.com/questions/29831489/convert-encoded_textay-of-indices-to-1-hot-encoded-numpy-encoded_textay
    '''
    # Create a placeholder for zeros.
    one_hot = np.zeros((encoded_text.size, num_uni_chars))
    
    # Convert data type for later use with pytorch (errors if we dont!)
    one_hot = one_hot.astype(np.float32)

    # Using fancy indexing fill in the 1s at the correct index locations
    one_hot[np.arange(one_hot.shape[0]), encoded_text.flatten()] = 1.0
    

    # Reshape it so it matches the batch sahe
    one_hot = one_hot.reshape((*encoded_text.shape, num_uni_chars))
    
    return one_hot

def main():
    # text data
    df = pd.read_parquet('data/finance_en.parquet')

    # encode text
    text = ' '.join(df['output'].values)

    all_characters = set(text)

    decoder = dict(enumerate(all_characters))

    encoder = {char: ind for ind,char in decoder.items()}

    encoded_text = np.array([encoder[char] for char in text])
    print(encoded_text)

if __name__ == "__main__":
    main()

