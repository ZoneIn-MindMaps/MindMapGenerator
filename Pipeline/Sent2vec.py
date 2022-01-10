import sent2vec
model = sent2vec.Sent2vecModel()
model.load_model('model.bin')
emb = model.embed_sentence("once upon a time .") 
embs = model.embed_sentences(["first sentence .", "another sentence"])