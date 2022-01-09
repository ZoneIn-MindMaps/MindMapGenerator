import KeyBERT, spaCy, SentenceTransformerEmbeddings, KMeansClustering
import pandas as pd
import nltk
import yake
from rake_nltk import Rake
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
stop_words = stopwords.words('english')
stopwords_dict = Counter(stop_words)
# from WordVectorGenerators import SentenceTransformerEmbeddings
# from ClusteringAlgorithms import KMeansClustering
class Pipeline:
    def __init__(self, KeyPhraseExtractor, WordEmbeddingName, ClusteringAlgorithmName):
        self.KeyPhraseExtractor = KeyPhraseExtractor
        self.WordEmbeddingName = WordEmbeddingName
        self.ClusteringAlgorithmName = ClusteringAlgorithmName
    def KeyPhraseExtraction(self, list_of_sentences, n_gram_range, top_n, nr_candidates, club_sentences):
        clubbed_sentences = []
        count = 0
        s = ""
        for i in range(len(list_of_sentences)):
            if (count < club_sentences):
                s += list_of_sentences[i] + " "
                count+=1
            if (count == club_sentences):
                clubbed_sentences.append(s)
                s = ""
                count = 0
        if (self.KeyPhraseExtractor == "KeyBERT"):
            return KeyBERT.Generate_KeyBERT_KeyPhrases(clubbed_sentences, n_gram_range, top_n, nr_candidates)
        elif (self.KeyPhraseExtractor == "spaCy"):
            return spaCy.Generate_spaCy_KeyPhrases(clubbed_sentences, top_n)
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
            for i in range(len(clubbed_sentences)):
                ls.append(custom_kw_extractor.extract_keywords(text))
            return ls
        elif (self.KeyPhraseExtractor == 'RAKE NLTK'):
            r = Rake()
            r.extract_keywords_from_sentences(clubbed_sentences)
            print(r.get_ranked_phrases())
            return r.extract_keywords_from_sentences(clubbed_sentences)
    def WordEmbeddingGenerator(self, list_of_sentences):
        if (self.WordEmbeddingName == "all-MiniLM-L6-v2"):
            return SentenceTransformerEmbeddings.getSentenceEmbeddings(list_of_sentences, "all-MiniLM-L6-v2")
        elif (self.WordEmbeddingName == "all-mpnet-base-v2"):
            return SentenceTransformerEmbeddings.getSentenceEmbeddings(list_of_sentences, "all-mpnet-base-v2")
    def WordClustering(self, WordEmbeddingList, n_clusters):
        if (self.ClusteringAlgorithmName == "KMeans"):
            return KMeansClustering.kmeans(WordEmbeddingList, n_clusters)
    

if __name__ == '__main__':
    df = pd.read_csv("/home/aflah20082/MindMapGenerator/Pipeline/transcript.csv")
    list_of_sentences = df['Text'].values.tolist()
    list_of_starttimes = df['Start Time'].values.tolist()
    list_of_duration = df['Duration'].values.tolist()
    list_of_endtimes = [sum(i) for i in zip(list_of_starttimes,list_of_duration)]
    list_of_non_stop_word_sentences = []
    list_of_non_stop_word_endtimes = []
    # print(list_of_starttimes[0])
    # print(list_of_duration[0])
    # print(list_of_endtimes[0])
    for i in range(len(list_of_sentences)):
        list_of_sentences[i] = list_of_sentences[i].lower()
    for i in range(len(list_of_sentences)):
        text = ' '.join([word for word in list_of_sentences[i].split() if word not in stopwords_dict])
        if (text == ""):
            print("Hello")
        else:
            list_of_non_stop_word_sentences.append(text)
            list_of_non_stop_word_endtimes.append(list_of_endtimes[i])
    # print(list_of_non_stop_word_sentences)
    # print(list_of_non_stop_word_endtimes)
    print(len(list_of_non_stop_word_endtimes), len(list_of_non_stop_word_sentences))
    pipeline = Pipeline("spaCy", "all-MiniLM-L6-v2", "KMeans")
    # print(list_of_non_stop_word_sentences)
    KeyPhraseList = pipeline.KeyPhraseExtraction(list_of_non_stop_word_sentences, 2, 10, 10, 10)
    print(KeyPhraseList)
    # KeyPhrases = []
    # for i in KeyPhraseList:
    #     for j in i:
    #         KeyPhrases.append(j[0])
    # print(KeyPhrases)
    # n_gram_range = (1, 1)
    # top_n = 3
    # nr_candidates = 3
    # n_clusters = 3
    # pipeline = Pipeline("KeyBERT", "all-mpnet-base-v2", "KMeans")
    # clubbedKeyPhrases = pipeline.KeyPhraseExtraction(list_of_non_stop_word_sentences, n_gram_range, top_n, nr_candidates, 5)
    # WordEmbeddingList = pipeline.WordEmbeddingGenerator(clubbedKeyPhrases)
    # print(clubbedKeyPhrases)
    # print()
    # print(WordEmbeddingList)
    # # with open("/home/aflah20082/Pipeline/KeyPhrases.txt", "w") as f:
    # #     for i in range(len(clubbedKeyPhrases)):
    # #         f.write(clubbedKeyPhrases[i] + "\n")
    # # with open("/home/aflah20082/Pipeline/WordEmbeddings.txt", "w") as f:
    # #     for i in range(len(WordEmbeddingList)):
    # #         f.write(str(WordEmbeddingList[i]) + "\n")
    # cluster_centers, cluster_labels = pipeline.WordClustering(WordEmbeddingList, n_clusters)
    # # with open("/home/aflah20082/Pipeline/ClusterCenters.txt", "w") as f:
    # #     for i in range(len(cluster_centers)):
    # #         f.write(str(cluster_centers[i]) + "\n")
    # print(cluster_centers)
    # print(cluster_labels)
    # print(list_of_non_stop_word_endtimes)