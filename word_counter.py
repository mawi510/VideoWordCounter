from collections import Counter
import string

def get_word_counts(segments):
    words = []
    word_times = {}
    for segment in segments:
        for word_info in segment['words']:
            word = word_info['word'].lower().strip().translate(str.maketrans('', '', string.punctuation))
            words.append(word)
            word_times.setdefault(word, []).append(word_info['start'])
    counter = Counter(words)
    return counter, word_times