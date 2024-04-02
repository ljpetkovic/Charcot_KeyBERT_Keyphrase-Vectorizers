from keyphrase_vectorizers import KeyphraseCountVectorizer
from keybert import KeyBERT
from flair.embeddings import TransformerDocumentEmbeddings
import os

docs = ["""Troubles trophiques consécutifs aux lésions des nerfs.
Sommaire. — Remarques préliminaires. — Objet des conférences de cette année : 
elles seront consacrées à celles des maladies du système nerveux et, en particulier, 
de la moelle épinière, que l'on observe le plus habituelle-ment à la Salpêtrière.
— Troubles de nutrition consécutifs aux lésions de l'axe cérébro-spinal et des nerfs. 
— Ces altérations peuvenl occuper la peau, le tissu cellulaire, les muscles, les articulations, les viscères.
Importance de ces altérations au point de vue du diagnostic et du pronostic. 
— Troubles de nu-trition consécutifs aux lésions des nerfs périphériques. 
— Le système ner-veux, à l'état normal, a peu d'influence sur l'accomplissement des actes nu-tritifs. 
— Les lésions passives des nerfs ou de la moelle ne produisent pas directement de troubles 
trophiques dans les parties périphériques : expé-riences qui le démontrent. — 
Influence de l'irritation et de l'inflammation des nerfs ou des centres nerveux sur la 
production des troubles trophiques. — Les troubles trophiques consécutifs aux lésions 
traumatiques des nerfs, considérés en particulier. — Ils résultent non des sections 
complètes, mais des sections incomplètes, des contusions, etc., des troncs nerveux. 
— Érup-tions cutanées diverses : Érythcme, zona traumalique, pemphigus. — Glossy Skin 
des auteurs anglais. — Lésions musculaires : atrophie. — Lésions ar-ticulaires ; 
lésions osseuses : périostite, nécrose. —Troubles trophiques con-sécutifs aux lésions 
non traumatiques. — Troubles trophiques de l'œil, dans les cas de tumeur comprimant le 
trijumeau. — Inflammation des nerfs spi-naux, consécutive au cancer vertébral, à la 
pachyméningite spinale, à l'as-phyxie par la vapeur de charbon, etc. Eruptions cutanées 
diverses (zona, pemphigus, etc.), atrophie musculaire, arthropathies, qui, en pareil cas, 
se développent en conséquence de la névrite. —Lèpre anesthésique : périné-vrite lépreuse, 
lepra mutilans.
               """]

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