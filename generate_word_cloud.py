from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(counter):
    wc = WordCloud(width=800, height=400, background_color='white')
    wc.generate_from_frequencies(counter)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()