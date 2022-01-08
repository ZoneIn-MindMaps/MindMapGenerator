from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import itertools

def Generate_KeyBERT_KeyPhrases(list_of_sentences, n_gram_range, top_n, nr_candidates):
    KeyPhraseList = []
    stop_words = "english"
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    for i in list_of_sentences:
        try:
            doc = i
            count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([doc])
            candidates = count.get_feature_names()
            model = SentenceTransformer('distilbert-base-nli-mean-tokens')
            doc_embedding = model.encode([doc])
            candidate_embeddings = model.encode(candidates)
            distances = cosine_similarity(doc_embedding, candidate_embeddings)
            keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
            KeyPhraseList.append(keywords)
        except ValueError:
            continue
    return KeyPhraseList

if __name__ == '__main__':
    list_of_sentences = [
        "The quick brown fox jumps over the lazy dog",
        "The five boxing wizards jump quickly"
    ]
    print(Generate_KeyBERT_KeyPhrases(list_of_sentences, (3, 3), 5, 5))