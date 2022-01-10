from flask import Flask, jsonify
import pandas as pd
from srt_parser import get_transcript
from pipeline import *
import nltk
import matplotlib.pyplot as plt
from WordCloud import show_wordcloud
from makeMindMap import makeGraph
import seaborn as sns
# nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
stop_words = stopwords.words('english')
stopwords_dict = Counter(stop_words)
app = Flask(__name__)

def time_format(seconds: int):
    if seconds is not None:
        seconds = int(seconds)
        d = seconds // (3600 * 24)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        if d > 0:
            return '{:02d}:{:02d}:{:02d}:{:02d}'.format(d, h, m, s)
        elif h > 0:
            return '{:02d}:{:02d}:{:02d}'.format(h, m, s)
        elif m > 0:
            return '{:02d}:{:02d}'.format(m, s)
        elif s > 0:
            return '00:{:02d}'.format(s)
    return '-'

"""
Default route
"""
@app.route('/')
def index():
    return "Hello World!"


# """
# API Which Takes String Input
# """
# @app.route('/<string:input>', methods=['GET'])
# def main(input):
#     print(input)
#     get_transcript(input)
#     df = pd.read_csv("/home/zoners/MindMapGenerator/Pipeline/transcript.csv")
#     list_of_sentences = df['Text'].values.tolist()
#     list_of_starttimes = df['Start Time'].values.tolist()
#     list_of_duration = df['Duration'].values.tolist()
#     list_of_endtimes = [sum(i) for i in zip(list_of_starttimes,list_of_duration)]
#     list_of_non_stop_word_sentences = []
#     list_of_non_stop_word_endtimes = []
#     for i in range(len(list_of_sentences)):
#         list_of_sentences[i] = list_of_sentences[i].lower()
#     for i in range(len(list_of_sentences)):
#         text = ' '.join([word for word in list_of_sentences[i].split() if word not in stopwords_dict])
#         if (text == ""):
#             continue
#         else:
#             list_of_non_stop_word_sentences.append(text)
#             list_of_non_stop_word_endtimes.append(list_of_endtimes[i])
#     list_of_non_stop_word_endtimes_clubbed = []
#     count = 0
#     club_times = 10
#     for i in range(len(list_of_non_stop_word_endtimes)):
#         if (count < club_times):
#             count+=1
#         if (count == club_times):
#             list_of_non_stop_word_endtimes_clubbed.append(list_of_non_stop_word_endtimes[i])
#             count = 0
#     count = 0
#     clubbed_sentence = []
#     s = ""
#     club_sentences = 10
#     for i in range(len(list_of_sentences)):
#         if (count < club_sentences):
#             s += list_of_sentences[i]
#             s += " "
#             count+=1
#         if (count == club_sentences):
#             clubbed_sentence.append(s)
#             s = ""
#             count = 0
#     pipeline = Pipeline("spaCy", "all-MiniLM-L6-v2", "KMeans")
#     KeyPhraseList = pipeline.KeyPhraseExtraction(clubbed_sentence, None, 3, None, 5)
#     WordEmbeddingList = pipeline.WordEmbeddingGenerator(KeyPhraseList, False)
#     TopicList = pipeline.KeyPhraseExtraction(clubbed_sentence, None, 1, None, 1)
#     cluster_count = 4
#     cluster_position, cluster_labels = pipeline.WordClustering(WordEmbeddingList, cluster_count)
#     ls_cluster_wise_key_words = [[] for i in range(cluster_count)]
#     for i in range(len(cluster_labels)):
#         x = cluster_labels[i]
#         ls_cluster_wise_key_words[x].append(clubbed_sentence[i])
#     print(ls_cluster_wise_key_words)
#     print(ls_cluster_wise_key_words)
#     for i in range(len(list_of_non_stop_word_endtimes_clubbed)):
#         list_of_non_stop_word_endtimes_clubbed[i] = time_format(int(list_of_non_stop_word_endtimes_clubbed[i]))
#     makeGraph(cluster_labels, list_of_non_stop_word_endtimes_clubbed)
#     for index, word_list in enumerate(ls_cluster_wise_key_words):
#         show_wordcloud(word_list, index)
#     return "Done"

"""
route that takes int input
"""
@app.route('/<int:input>', methods=['GET'])
def main_int(input):
    print("Hello here")
    ls = []
    with open("/home/zoners/ZoneIn-Organisation/uploads/test_links/link.txt", "r") as f:
        ls = f.readlines()
    link = ls[0]
    link = link[len(link)-11:]
    get_transcript(link)
    df = pd.read_csv("/home/zoners/MindMapGenerator/Pipeline/transcript.csv")
    list_of_sentences = df['Text'].values.tolist()
    list_of_starttimes = df['Start Time'].values.tolist()
    list_of_duration = df['Duration'].values.tolist()
    list_of_endtimes = [sum(i) for i in zip(list_of_starttimes,list_of_duration)]
    list_of_non_stop_word_sentences = []
    list_of_non_stop_word_endtimes = []
    for i in range(len(list_of_sentences)):
        list_of_sentences[i] = list_of_sentences[i].lower()
    for i in range(len(list_of_sentences)):
        text = ' '.join([word for word in list_of_sentences[i].split() if word not in stopwords_dict])
        if (text == ""):
            continue
        else:
            list_of_non_stop_word_sentences.append(text)
            list_of_non_stop_word_endtimes.append(list_of_endtimes[i])
    list_of_non_stop_word_endtimes_clubbed = []
    count = 0
    club_times = 10
    for i in range(len(list_of_non_stop_word_endtimes)):
        if (count < club_times):
            count+=1
        if (count == club_times):
            list_of_non_stop_word_endtimes_clubbed.append(list_of_non_stop_word_endtimes[i])
            count = 0
    count = 0
    clubbed_sentence = []
    s = ""
    club_sentences = 10
    for i in range(len(list_of_sentences)):
        if (count < club_sentences):
            s += list_of_sentences[i]
            s += " "
            count+=1
        if (count == club_sentences):
            clubbed_sentence.append(s)
            s = ""
            count = 0
    pipeline = Pipeline("spaCy", "all-MiniLM-L6-v2", "KMeans")
    KeyPhraseList = pipeline.KeyPhraseExtraction(clubbed_sentence, None, 3, None, 5)
    WordEmbeddingList = pipeline.WordEmbeddingGenerator(KeyPhraseList, False)
    TopicList = pipeline.KeyPhraseExtraction(clubbed_sentence, None, 1, None, 1)
    cluster_count = 4
    cluster_position, cluster_labels = pipeline.WordClustering(WordEmbeddingList, cluster_count)
    ls_cluster_wise_key_words = [[] for i in range(cluster_count)]
    for i in range(len(cluster_labels)):
        x = cluster_labels[i]
        ls_cluster_wise_key_words[x].append(clubbed_sentence[i])
    print(ls_cluster_wise_key_words)
    print(ls_cluster_wise_key_words)
    for i in range(len(list_of_non_stop_word_endtimes_clubbed)):
        list_of_non_stop_word_endtimes_clubbed[i] = time_format(int(list_of_non_stop_word_endtimes_clubbed[i]))
    makeGraph(cluster_labels, list_of_non_stop_word_endtimes_clubbed)
    for index, word_list in enumerate(ls_cluster_wise_key_words):
        show_wordcloud(word_list, index)
    return "Done with txt"

if __name__ == '__main__':
    app.run(debug=True)