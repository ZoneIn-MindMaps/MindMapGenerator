from sentence_transformers import SentenceTransformer
from sentence_transformers import util

def getSentenceEmbeddings(sentenceList, modelName):
    model = SentenceTransformer(modelName)
    sentence_embeddings = model.encode(sentenceList)
    return sentence_embeddings

if __name__ == '__main__':
    list_of_sentences = [['jumps lazy dog', 'quick brown fox', 'brown fox jumps', 'fox jumps lazy'], ['wizards jump quickly', 'boxing wizards jump']]
    print(getSentenceEmbeddings(list_of_sentences, 'bert-base-nli-mean-tokens'))