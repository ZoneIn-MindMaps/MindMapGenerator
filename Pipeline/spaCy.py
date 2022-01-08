import spacy
import pytextrank
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")

def Generate_spaCy_KeyPhrases(list_of_sentences, top_n):
    KeyPhraseList = []
    for i in list_of_sentences:
        doc = nlp(i)
        ls = []
        for phrase in doc._.phrases:
            ls.append(phrase.text)
        if (len(ls) > top_n):
            ls = ls[:top_n]
        KeyPhraseList.append(ls)
    return KeyPhraseList

if __name__ == '__main__':
    list_of_sentences = [
        "The quick brown fox jumps over the lazy dog",
        "The five boxing wizards jump quickly"
    ]
    print(Generate_spaCy_KeyPhrases(list_of_sentences, 5))
