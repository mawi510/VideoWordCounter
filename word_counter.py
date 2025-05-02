from collections import Counter
import string
import re

#This allows the user to see where a word was said
#However we want to eliminate stop words as they're not super informative/interesting

import nltk
from nltk.corpus import stopwords

#Have to download stopwords first
nltk.download('stopwords')

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

def clean_word(word):
    return emoji_pattern.sub(r'', word.lower().strip().translate(str.maketrans('', '', string.punctuation)))

def get_word_counts(segments):
    words = []
    word_times = {}
    for segment in segments:
        for word_info in segment['words']:
            word = clean_word(word_info['word'])
            if word not in stopwords.words('english') and word != '':
                words.append(word)
                word_times.setdefault(word, []).append(word_info['start'])
    counter = Counter(words)
    return counter, word_times