import KeyBERT, spaCy, SentenceTransformerEmbeddings, KMeansClustering, HierarchicalClustering
import pandas as pd
import nltk
import matplotlib.pyplot as plt
import yake
from makeMindMap import makeGraph
from dbscan import DBSCANClusters
import tensorflow_hub as hub
from sklearn.preprocessing import StandardScaler
from transformers import AutoModel
import seaborn as sns
from rake_nltk import Rake
from sklearn.decomposition import PCA
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
stop_words = stopwords.words('english')
stopwords_dict = Counter(stop_words)
# from WordVectorGenerators import SentenceTransformerEmbeddings
# from ClusteringAlgorithms import KMeansClustering

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

class Pipeline:
    def __init__(self, KeyPhraseExtractor, WordEmbeddingName, ClusteringAlgorithmName):
        self.KeyPhraseExtractor = KeyPhraseExtractor
        self.WordEmbeddingName = WordEmbeddingName
        self.ClusteringAlgorithmName = ClusteringAlgorithmName
    def KeyPhraseExtraction(self, list_of_sentences, n_gram_range, top_n, nr_candidates, club_sentences):
        if (self.KeyPhraseExtractor == "KeyBERT"):
            return KeyBERT.Generate_KeyBERT_KeyPhrases(list_of_sentences, n_gram_range, top_n, nr_candidates)
        elif (self.KeyPhraseExtractor == "spaCy"):
            KeyPhraseList = spaCy.Generate_spaCy_KeyPhrases(list_of_sentences, top_n)
            ls = []
            for i in KeyPhraseList:
                ls.append(" ".join(i))
            return ls
        elif (self.KeyPhraseExtractor == "YAKE"):
            kw_extractor = yake.KeywordExtractor()
            language = "en"
            max_ngram_size = 3
            deduplication_thresold = 0.9
            deduplication_algo = 'seqm'
            windowSize = 1
            numOfKeywords = 20
            custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
            ls = []
            for i in range(len(list_of_sentences)):
                ls.append(custom_kw_extractor.extract_keywords(text))
            return ls
        elif (self.KeyPhraseExtractor == 'RAKE NLTK'):
            r = Rake()
            r.extract_keywords_from_sentences(list_of_sentences)
            print(r.get_ranked_phrases())
            return r.extract_keywords_from_sentences(list_of_sentences)
    def WordEmbeddingGenerator(self, list_of_sentences, club_sentences):
        if (self.WordEmbeddingName == "all-MiniLM-L6-v2"):
            return SentenceTransformerEmbeddings.getSentenceEmbeddings(list_of_sentences, "all-MiniLM-L6-v2")
        elif (self.WordEmbeddingName == "all-mpnet-base-v2"):
            return SentenceTransformerEmbeddings.getSentenceEmbeddings(list_of_sentences, "all-mpnet-base-v2")
        elif (self.WordEmbeddingName == "BERT-Mini"):
            model = AutoModel.from_pretrained("prajjwal1/bert-mini")
            ls = []
            for i in list_of_sentences:
                ls.append(model.encode(i))
            return ls
        elif (self.WordEmbeddingName == "Universal Sentence Encoder"):
            model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
            ls = []
            for i in list_of_sentences:
                ls.append(model.predict(i))
            return ls
    def WordClustering(self, WordEmbeddingList, n_clusters):
        if (self.ClusteringAlgorithmName == "KMeans"):
            return KMeansClustering.kmeans(WordEmbeddingList, n_clusters)
        elif (self.ClusteringAlgorithmName == "DBSCAN"):
            return DBSCANClusters(WordEmbeddingList)
        elif (self.ClusteringAlgorithmName == "Agglomerative"):
            return HierarchicalClustering.HierarchicalClusters(WordEmbeddingList)

if __name__ == '__main__':
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
    # print(list_of_non_stop_word_sentences)
    # print(list_of_non_stop_word_endtimes)

    # Clubbing Time
    list_of_non_stop_word_endtimes_clubbed = []
    count = 0
    club_times = 10
    for i in range(len(list_of_non_stop_word_endtimes)):
        if (count < club_times):
            count+=1
        if (count == club_times):
            list_of_non_stop_word_endtimes_clubbed.append(list_of_non_stop_word_endtimes[i])
            count = 0
    #Clubbing Sentences
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
    cluster_position, cluster_labels = pipeline.WordClustering(WordEmbeddingList, 4)
    print(cluster_labels)
    print("list_of_non_stop_word_endtimes_clubbed")
    for i in range(len(list_of_non_stop_word_endtimes_clubbed)):
        list_of_non_stop_word_endtimes_clubbed[i] = time_format(int(list_of_non_stop_word_endtimes_clubbed[i]))
    print(list_of_non_stop_word_endtimes_clubbed)
    print (len(KeyPhraseList), len(WordEmbeddingList), len(TopicList), len(cluster_labels), len(list_of_non_stop_word_endtimes_clubbed))
    makeGraph(cluster_labels, list_of_non_stop_word_endtimes_clubbed)