##########################################################
# An attempt at writting a custom markov chain to generate
# text based on my company's blog posts
#
# bcutrell13@gmail.com - April 2019
##########################################################

##########################################################
# Imports
##########################################################
import glob
import requests
from bs4 import BeautifulSoup

import numpy as np
from nltk.tokenize import word_tokenize
import random as rm

##########################################################
# Constants
##########################################################
SAMPLE_URL = 'https://www.fake.com/our-thinking/fake-blog/release-nexgen-social-screens'

#############################
# Functions
#############################
def get_text():
    page = requests.get(SAMPLE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    post_p_tags = soup.find(class_='post-body').find_all('p')
    text = [p.get_text() for p in post_p_tags]
    return ' '.join(text)

def read_files():
    filenames = glob.glob('blog_posts/*.txt')

    text = ''
    for filename in filenames:
        file = open(filename, 'rt')
        text += file.read()
        file.close()
    return text

def text_to_words(text):
    tokens = word_tokenize(text)
    return [word for word in tokens if word.isalpha()]

# find all the pairs of words
def make_pairs(words):
    for i in range(len(words)-1):
        yield (words[i], words[i+1])

def word_forecast(words, n_words):
    pairs = make_pairs(words)

    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    first_word = np.random.choice(words)
    chain = [first_word]

    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))
    return ' '.join(chain)

#############################
# Run
#############################
def run():
    text = read_files()
    words = text_to_words(text)
    return word_forecast(words, 60)

#############################
# Main
#############################
if __name__ == "__main__":
    print(run())
