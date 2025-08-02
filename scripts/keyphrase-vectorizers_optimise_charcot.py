!pip install keyphrase-vectorizers
!pip install keybert
!pip install flair
!pip install spacy
!python -m spacy download fr_core_news_lg


import glob
import os
import csv
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
from flair.embeddings import TransformerDocumentEmbeddings
import spacy

# Load the spaCy model
nlp = spacy.load("fr_core_news_lg")

# Convert spaCy's stop words to a list
# french_stop_words = list(nlp.Defaults.stop_words)

# Set input/output paths
input_path = "/Users/ljudmilapetkovic/Library/CloudStorage/Dropbox/ObTIC/CHARCOT/Charcot_KeyBERT_Keyphrase-Vectorizers/corpus/txt_corpus_Charcot/"
output_file_name = "/Users/ljudmilapetkovic/Library/CloudStorage/Dropbox/ObTIC/CHARCOT/Charcot_KeyBERT_Keyphrase-Vectorizers/output/kpv_charcot_sacado.csv"

# Use CamemBERT model (best for French)
kw_model = KeyBERT(model=TransformerDocumentEmbeddings("camembert-base"))

# Setup vectorizer with a well-formed pattern
vectorizer = KeyphraseCountVectorizer(
    spacy_pipeline=nlp,
    pos_pattern=(
       # "<NOUN>+"                                 # NOM ou plusieurs NOM
        "<NOUN>+<NOUN>+"                         # NOM + NOM
        "|<NOUN>+<ADJ>+"                          # NOM + ADJ
        "|<NOUN>+<ADJ>+<ADJ>*"                    # NOM + plusieurs ADJ
        "|<NOUN>+<ADP><NOUN>+"                    # NOM + PRÉP + NOM
        "|<NOUN>+<ADP><NOUN>+<ADJ>*"              # NOM + PRÉP + NOM + (ADJ*)
        "|<NOUN>+<ADP><NOUN>+<ADJ>+<ADJ>*"        # NOM + PRÉP + NOM + plusieurs ADJ
    )
    # stop_words=french_stop_words
)


# Get all .txt files in the input directory
input_files = glob.glob(os.path.join(input_path, "*.txt"))

# Open CSV file for writing
with open(output_file_name, "w", encoding="utf-8", newline="") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=";")
    csv_writer.writerow(["Filename", "Keyphrase", "Score"])  # Header row

    # Process each file in the directory
    for input_file_name in input_files:
        print(f"Processing file: {input_file_name}")

        with open(input_file_name, "r", encoding="utf-8") as input_file:
            buffer = []  # Temporary storage for processing
            line_count = 0  # Track lines processed
            
            for line in input_file:
                if line.strip():  # Avoid empty lines
                    buffer.append(line.strip())  # Store line in buffer
                    line_count += 1

                if line_count % 500 == 0 and buffer:  # Process every 500 lines
                    data = " ".join(buffer)  # Convert buffer to a string
                    buffer = []  # Clear buffer after processing

                    try:
                        keyphrases = kw_model.extract_keywords(data, vectorizer=vectorizer)
                        if keyphrases:  # Ensure we have extracted phrases
                            for phrase, score in keyphrases:
                                csv_writer.writerow([os.path.basename(input_file_name), phrase, f"{score:.4f}"])
                    except ValueError as e:
                        print(f"Error processing {input_file_name} at line {line_count}: {e}")

            # Process any remaining lines in the buffer
            if buffer:
                data = " ".join(buffer)
                try:
                    keyphrases = kw_model.extract_keywords(data, vectorizer=vectorizer)
                    if keyphrases:  # Ensure we have extracted phrases
                        for phrase, score in keyphrases:
                            csv_writer.writerow([os.path.basename(input_file_name), phrase, f"{score:.4f}"])
                except ValueError as e:
                    print(f"Error processing {input_file_name} at end of file: {e}")

print(f"Keyphrases saved to {output_file_name}")
