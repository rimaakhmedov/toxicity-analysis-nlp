import nltk
import pymorphy3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

MODEL_PATH = r'model/ta-model'

nltk.download('stopwords')
nltk.download('punkt')

tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
morph = pymorphy3.MorphAnalyzer()
stop_words = stopwords.words("russian")
model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))


def preprocess_text(text):
    pattern = re.compile(r'[a-zA-Zа-яА-Я]+', re.UNICODE)
    words = re.findall(pattern, text)

    words = word_tokenize(' '.join(words), language='russian')
    filtered_words = [word for word in words if word.lower() not in stop_words]

    lemmatized_words = [morph.parse(word)[0].normal_form for word in filtered_words]

    return ' '.join(lemmatized_words)



def preprocess_and_predict(text: str):
  preprocessed = preprocess_text(text)
  tokenized = tokenizer(preprocessed, return_tensors="pt")


  with torch.no_grad():
    outputs = model(**tokenized)

  predictions = torch.softmax(outputs.logits, dim=1).tolist()[0]

  return predictions