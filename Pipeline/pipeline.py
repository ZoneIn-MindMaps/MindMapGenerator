import KeyBERT, spaCy, SentenceTransformerEmbeddings, KMeansClustering
import pandas as pd
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
    def WordEmbeddingGenerator(self, list_of_sentences):
        if (self.WordEmbeddingName == "all-MiniLM-L6-v2"):
            return SentenceTransformerEmbeddings.getSentenceEmbeddings(list_of_sentences, "all-MiniLM-L6-v2")
        elif (self.WordEmbeddingName == "all-mpnet-base-v2"):
            return SentenceTransformerEmbeddings.getSentenceEmbeddings(list_of_sentences, "all-mpnet-base-v2")
    def WordClustering(self, WordEmbeddingList, n_clusters):
        if (self.ClusteringAlgorithmName == "KMeans"):
            return KMeansClustering.kmeans(WordEmbeddingList, n_clusters)
    

if __name__ == '__main__':
    df = pd.read_csv("/home/aflah20082/Pipeline/transcript.csv")
    list_of_sentences = df['Text'].values.tolist()
    n_gram_range = (1, 1)
    top_n = 3
    nr_candidates = 3
    n_clusters = 3
    pipeline = Pipeline("KeyBERT", "all-mpnet-base-v2", "KMeans")
    clubbedKeyPhrases = pipeline.KeyPhraseExtraction(list_of_sentences, n_gram_range, top_n, nr_candidates, 5)
    WordEmbeddingList = pipeline.WordEmbeddingGenerator(clubbedKeyPhrases)
    print(clubbedKeyPhrases)
    print()
    print(WordEmbeddingList)
    # with open("/home/aflah20082/Pipeline/KeyPhrases.txt", "w") as f:
    #     for i in range(len(clubbedKeyPhrases)):
    #         f.write(clubbedKeyPhrases[i] + "\n")
    # with open("/home/aflah20082/Pipeline/WordEmbeddings.txt", "w") as f:
    #     for i in range(len(WordEmbeddingList)):
    #         f.write(str(WordEmbeddingList[i]) + "\n")
    cluster_centers, cluster_labels = pipeline.WordClustering(WordEmbeddingList, n_clusters)
    # with open("/home/aflah20082/Pipeline/ClusterCenters.txt", "w") as f:
    #     for i in range(len(cluster_centers)):
    #         f.write(str(cluster_centers[i]) + "\n")
    print(cluster_centers, cluster_labels)