from top2vec import Top2Vec
import pandas as pd
df = pd.read_csv("/home/aflah20082/MindMapGenerator/Pipeline/transcript2.csv")
list_of_sentences = df['Text'].values.tolist()
model = Top2Vec(list_of_sentences)
print(model)
