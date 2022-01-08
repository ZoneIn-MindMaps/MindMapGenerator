from flask import Flask, jsonify
import pandas as pd
from Pipeline import pipeline
from SRT_Parser import srt_parser
app = Flask(__name__)

"""
API Which Takes String Input
"""
@app.route('/<string:input>', methods=['GET'])
def get_transcript(input):
    srt_parser.get_transcript(input)
    df = pd.read_csv("/home/aflah20082/Pipeline/transcript.csv")
    list_of_sentences = df['Text'].values.tolist()
    n_gram_range = (1, 1)
    top_n = 3
    nr_candidates = 3
    n_clusters = 3
    Clusterer = pipeline.Pipeline("KeyBERT", "all-mpnet-base-v2", "KMeans")
    clubbedKeyPhrases = Clusterer.KeyPhraseExtraction(list_of_sentences, n_gram_range, top_n, nr_candidates, 5)
    WordEmbeddingList = Clusterer.WordEmbeddingGenerator(clubbedKeyPhrases)
    cluster_centers, cluster_labels = Clusterer.WordClustering(WordEmbeddingList, n_clusters)
    return (clubbedKeyPhrases, WordEmbeddingList, cluster_centers, cluster_labels)

if __name__ == '__main__':
    app.run(debug=True)