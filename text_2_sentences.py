import os
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import chardet


filepath = input('filepath:')
with open(filepath, 'rb') as f:
    rawdata = f.read()
    result = chardet.detect(rawdata)
    print(result)
    text = rawdata.decode(result['encoding'])
print(text)

# Remove extra whitespace
text = re.sub('\s+', ' ', text)
# Remove punctuation
text = re.sub('[^\w\s]', '', text)
# Remove non-alphanumeric characters
text = re.sub('[^0-9a-zA-Z\s]+', '', text)
# Lowercase the text
text = text.lower()

# Tokenize the text
tokens = nltk.word_tokenize(text)
# Lemmatize the tokens
lemmatizer = WordNetLemmatizer()
tokens = [lemmatizer.lemmatize(token) for token in tokens]
cleaned_text = ' '.join(tokens)


'''
below 
LookupError: 
**********************************************************************
  Resource averaged_perceptron_tagger not found.
  Please use the NLTK Downloader to obtain the resource:

import nltk
nltk.download('averaged_perceptron_tagger')
'''

# Tokenize the cleaned text into sentences
sentences = sent_tokenize(cleaned_text)

# Loop through each sentence
for i, sentence in enumerate(sentences):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    # Add part-of-speech tags to each word
    tagged_words = nltk.pos_tag(words)

    # Add capitalization and punctuation to the sentence
    reconstructed_sentence = ""
    for j, (word, tag) in enumerate(tagged_words):
        if j == 0:
            # Capitalize the first word of the sentence
            reconstructed_sentence += word.capitalize()
        else:
            # Add punctuation if the previous word was an end-of-sentence punctuation
            if tagged_words[j - 1][1] in [".", "!", "?"]:
                reconstructed_sentence += " "
            # Add a space between words
            else:
                reconstructed_sentence += " "
            # Add the current word
            reconstructed_sentence += word

    # Add end-of-sentence punctuation
    if tagged_words[-1][1] not in [".", "!", "?"]:
        reconstructed_sentence += "."

    # Replace the original sentence with the reconstructed sentence
    sentences[i] = reconstructed_sentence

# Join the sentences back into a single string
reconstructed_text = " ".join(sentences)











basename = os.path.basename(filepath)
basename_cleaned = os.path.splitext(basename)[0] + "_cleaned" + os.path.splitext(basename)[1]
filepath_cleaned = os.path.join(os.path.dirname(filepath), basename_cleaned)
with open(filepath_cleaned, 'w') as f:
    f.write(cleaned_text)
