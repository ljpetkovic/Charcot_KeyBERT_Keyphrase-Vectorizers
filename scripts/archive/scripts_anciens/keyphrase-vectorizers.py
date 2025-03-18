# Pré-requis :
# 1. GPU (sinon, CPU)
#    - si mémoire RAM épuisée, penser à vider la mémoire cache
# 2. excellente connexion de réseau

# Installations
!pip install keyphrase-vectorizers
!pip install deplacy spacy-transformers
!python -m spacy download fr_core_news_lg

# Imports
import spacy
from google.colab import drive
from keyphrase_vectorizers import KeyphraseCountVectorizer
import os

# Charger le modèle français spaCy_lg
nlp = spacy.load("fr_core_news_lg")

# Monter le Google Drive
drive.mount('/content/drive')

# Initialiser le vectoriseur avec le modèle spécifié
vectorizer = KeyphraseCountVectorizer(spacy_pipeline=nlp, pos_pattern='<N.*>*<ADJ.*>*<ADJ.*>+', stop_words='french')

# Définir les chemins vers les fichiers d'entrée et de sortie
path = '/content/drive/MyDrive/JE_ObTIC_Circulations/data/'
input_file_name = 'corpus_charcot.txt' # 'corpus_autres.txt' pour le corpus Autres
output_file_name = 'charcot_keyphrase-vectorizers.txt' # ou 'autres_keyphrase-vectorizers.txt' pour le corpus Autres

# Définir la fonction qui traite les blocs de texte (segmentation)
def process_chunk(chunk):
    # Join the lines into a single string
    data = " ".join(chunk)
    # Fit the vectorizer on the chunk
    vectorizer.fit([data])

# Lire le fichier et le traiter en blocs des 5,000 lignes pour éviter de charger l'intégralité du fichier en mémoire
# Dans le cas des blocs plus grands, la mémoire RAM s'épuise et la session Colab plante
chunk_size = 5000
current_chunk = []

with open(os.path.join(path, input_file_name), 'r') as myfile:
    for line in myfile:
        current_chunk.append(line.strip())
        if len(current_chunk) == chunk_size:
            process_chunk(current_chunk)
            current_chunk = []  # Reset the chunk

    # Traiter toutes les lignes restantes dans le dernier bloc
    if current_chunk:
        process_chunk(current_chunk)

# Après avoir traité tous les blocs, extraire et sauvegarder les mots-clés dans un fichier
keyphrases = vectorizer.get_feature_names_out()

with open(os.path.join(path, output_file_name), 'w') as output_file:
    for keyphrase in keyphrases:
        print(keyphrase)
        output_file.write(keyphrase + '\n')