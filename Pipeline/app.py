from flask import Flask, jsonify
import pandas as pd
from srt_parser import get_transcript
from pipeline import *
app = Flask(__name__)

"""
Default route
"""
@app.route('/')
def index():
    return "Hello World!"


"""
API Which Takes String Input
"""
@app.route('/<string:input>', methods=['GET'])
def abc(input):
    print(input)
    get_transcript(input)
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
    club_times = 5
    for i in range(len(list_of_non_stop_word_endtimes)):
        if (count < club_times):
            count+=1
        if (count == club_times):
            list_of_non_stop_word_endtimes_clubbed.append(list_of_non_stop_word_endtimes[i])
            count = 0
    print(len(list_of_non_stop_word_endtimes), len(list_of_non_stop_word_sentences), len(list_of_non_stop_word_endtimes_clubbed))
    pipeline = Pipeline("spaCy", "all-MiniLM-L6-v2", "Agglomerative")
    KeyPhraseList = pipeline.KeyPhraseExtraction(list_of_non_stop_word_sentences, 2, 10, 10, 10)
    print(KeyPhraseList)
    WordEmbeddingList = pipeline.WordEmbeddingGenerator(KeyPhraseList)
    print(WordEmbeddingList)
    clusters = pipeline.WordClustering(WordEmbeddingList, None)
    print(clusters)

if __name__ == '__main__':
    app.run(debug=True)