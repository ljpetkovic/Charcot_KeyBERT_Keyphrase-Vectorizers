# Installer KeyBERT et toutes les dépendances
!pip install keybert[all]

import torch # print(torch.__version__)
import os
from google.colab import drive
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT

# Monter le Google Drive
drive.mount('/content/drive')

# Definir les chemins vers les fichiers d'entrée et de sortie
path = '/content/drive/MyDrive/JE_ObTIC_Circulations/data/'
file_name = 'charcot_keybert_mmr.txt'
file_path = 'corpus_charcot.txt'

# Initialiser le modèle de phrase et le modèle KeyBERT
sentence_model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
kw_model = KeyBERT(model=sentence_model)

with open(os.path.join(path, file_name), 'w') as f:
    pass  # Pour vider le fichier


# Définir une fonction pour traiter des morceaux de texte
written_keywords = set()  # Garder une trace des mots-clés qui ont été écrits dans le fichier

def process_text_chunk(text_chunk):
    global written_keywords
    keywords = kw_model.extract_keywords(text_chunk, keyphrase_ngram_range=(1, 3), stop_words=None, use_mmr=True, diversity=0.7)
    with open(os.path.join(path, file_name), 'a+') as liste:
        for keyword, score in keywords:
            if keyword not in written_keywords:
                print(keyword)
                liste.write(keyword + '\n')
                written_keywords.add(keyword)



# Traitez le fichier en morceaux pour éviter de charger l'intégralité du fichier en mémoire
chunk_size = 300  # Définir le nombre de lignes à lire à la fois


try:
    with open(os.path.join(path, file_path), 'r') as file:
      lines_buffer = []
      for line in file:
          lines_buffer.append(line.strip())
          if len(lines_buffer) >= chunk_size:
              data = " ".join(lines_buffer)
              process_text_chunk(data)
              lines_buffer = []  # Réinitialiser le tampon après le traitement

      # Traiter tout le texte restant
      if lines_buffer:
          data = " ".join(lines_buffer)
          process_text_chunk(data)

except Exception as e:
    print(f"An error occurred: {e}")