from sentence_transformers import SentenceTransformer
from sentence_transformers import util

def getSentenceEmbeddings(sentenceList, modelName):
    model = SentenceTransformer(modelName)
    sentence_embeddings = model.encode(sentenceList)
    return sentence_embeddings
