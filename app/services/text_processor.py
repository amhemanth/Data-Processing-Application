import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
import random
from typing import Dict, Any

class TextProcessor:
    @staticmethod
    def process(text: str, preprocessing_options: Dict[str, bool], augmentation_options: Dict[str, bool]) -> Dict[str, str]:
        result = {"original": text, "preprocessed": text, "augmented": text}
        
        # Preprocessing
        if preprocessing_options.get("cleaning"):
            text = text.replace('\n', ' ').strip()
            text = ' '.join(text.split())
        
        if preprocessing_options.get("lowercase"):
            text = text.lower()
        
        if preprocessing_options.get("stopwords"):
            stop_words = set(stopwords.words('english'))
            words = word_tokenize(text)
            text = ' '.join([word for word in words if word.lower() not in stop_words])
        
        if preprocessing_options.get("stemming"):
            stemmer = PorterStemmer()
            words = word_tokenize(text)
            text = ' '.join([stemmer.stem(word) for word in words])
        
        if preprocessing_options.get("lemmatization"):
            lemmatizer = WordNetLemmatizer()
            words = word_tokenize(text)
            text = ' '.join([lemmatizer.lemmatize(word) for word in words])
        
        if preprocessing_options.get("tokenization"):
            text = ' '.join(word_tokenize(text))
        
        result["preprocessed"] = text
        
        # Augmentation
        if augmentation_options.get("synonym"):
            words = word_tokenize(text)
            augmented_words = []
            for word in words:
                synsets = wordnet.synsets(word)
                if synsets:
                    synonyms = [lemma.name() for synset in synsets for lemma in synset.lemmas()]
                    if synonyms:
                        augmented_words.append(random.choice(synonyms))
                    else:
                        augmented_words.append(word)
                else:
                    augmented_words.append(word)
            result["augmented"] = ' '.join(augmented_words)
        
        if augmentation_options.get("insertion"):
            words = word_tokenize(text)
            augmented_words = []
            for word in words:
                augmented_words.append(word)
                if random.random() < 0.3:
                    synsets = wordnet.synsets(word)
                    if synsets:
                        synonyms = [lemma.name() for synset in synsets for lemma in synset.lemmas()]
                        if synonyms:
                            augmented_words.append(random.choice(synonyms))
            result["augmented"] = ' '.join(augmented_words)
        
        return result 