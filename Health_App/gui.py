import nltk
from nltk.stem import WordNetLemmatizer
import validators
import pickle
import numpy as np
from tensorflow import keras
import json
import random
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure NLTK can find project-local nltk_data and try to auto-download 'punkt' if missing
PROJECT_ROOT = os.path.dirname(BASE_DIR)
NLTK_DATA_PATH = os.path.join(PROJECT_ROOT, 'nltk_data')
if NLTK_DATA_PATH not in nltk.data.path:
    nltk.data.path.append(NLTK_DATA_PATH)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except Exception:
        # If download fails, proceed — the view will handle missing resource at runtime.
        pass

# Define dynamic paths
MODEL_PATH = os.path.join(BASE_DIR, 'chatbot_model.h5')
INTENTS_PATH = os.path.join(BASE_DIR, 'intents.json')
WORDS_PATH = os.path.join(BASE_DIR, 'words.pkl')
CLASSES_PATH = os.path.join(BASE_DIR, 'classes.pkl')

# Load model and data using dynamic paths
model = None

# Ensure 'wordnet' and 'omw-1.4' are available; try auto-download if missing
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    try:
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
    except Exception:
        # If downloads fail (no network), we'll fall back gracefully below
        pass

lemmatizer = WordNetLemmatizer()

# Helper: safe lemmatize to avoid LookupError if NLTK corpora are missing
def safe_lemmatize(word):
    try:
        return lemmatizer.lemmatize(word.lower())
    except LookupError:
        return word.lower()

intents = json.loads(open(INTENTS_PATH).read())
words = pickle.load(open(WORDS_PATH, 'rb'))
classes = pickle.load(open(CLASSES_PATH, 'rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # lemmatize each word using safe wrapper
    sentence_words = [safe_lemmatize(word) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return (np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    print(p)
    res = model.predict(np.array([p]))[0]
    print(res)
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            print(result)
            # print("Predicted Class"+str(i['tag']))
            break
    return result


def chatbot_response(msg):
    # lazy-load model to avoid heavy import-time work
    global model
    if model is None:
        try:
            model = keras.models.load_model(MODEL_PATH, compile=False)
        except Exception as e:
            # propagate informative error so views can handle it
            raise
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    print(res)
    valid=validators.url(res)
    if valid==True:
        print("Url is valid")
    else:
        print("Invalid url")
    return res

