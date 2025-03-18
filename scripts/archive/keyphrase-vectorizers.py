from keyphrase_vectorizers import KeyphraseCountVectorizer
from keybert import KeyBERT
from flair.embeddings import TransformerDocumentEmbeddings
import os

# Définir les chemins vers les fichiers d'entrée et de sortie
path = '../corpus/'
input_file_name = 'corpus_Charcot.txt' # 'corpus_autres.txt' pour le corpus Autres
output_file_name = '../output/ckpv.txt' # ou 'autres_keyphrase-vectorizers.txt' pour le corpus Autres

# Init French KeyBERT model
kw_model = KeyBERT(model=TransformerDocumentEmbeddings('google-bert/bert-base-multilingual-cased'))

# Init vectorizer for the French language
vectorizer = KeyphraseCountVectorizer(spacy_pipeline='fr_core_news_lg', pos_pattern='<N.*><ADJ.*><ADJ.*>+', stop_words='french')

# Get French keyphrases
kp = kw_model.extract_keywords(docs=docs, vectorizer=vectorizer)

with open(os.path.join(path, output_file_name), 'w') as output_file:
    for k in kp:
        print(k)
        output_file.write(str(k) + '\n')