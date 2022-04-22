import pandas as pd
import numpy as np
from sklearn import *


import re

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer

from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import confusion_matrix, accuracy_score, classification_report




def Text_Processing(text, stop_words):
    
    # Suppression les nombres
    text = re.sub(r'\d+', '', text)

    #Suppression les saut de lignes
    text = re.sub('\n', '', text)
    
    #Séparation les mots de la variable text
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(text.lower())
    
    lemmatizer = WordNetLemmatizer()
    
    tokens_drop_stop_word = []
    for mot in tokens:
        if mot not in stop_words:
            tokens_drop_stop_word.append(lemmatizer.lemmatize(mot))
    
    return(" ".join(tokens_drop_stop_word))




def sentimens_analysis_predict(phrase):

    #chargement des données 
    df = pd.read_csv('https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/reviews.csv')

    # Ajout la variable expliquée
    df['Sentiment'] = df['Rating'].apply(lambda x: 0 if x < 3 else 1)

    #suppression des mots inutile
    mots_vide = ["also", "get", "going", "could", "however", "go", ")", "("]
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', ",", "?", "!", ";", ":", "-", "--", '"', "...", "..", "'", "i", "I", "they've", "they're", "they'll", "the", "so", "this", "in", "we're", "we've", "us", ""])
    stop_words.update(mots_vide)
    df.Review_Text = df.Review_Text.apply(lambda text: Text_Processing(text, stop_words))

    #preparation de données
    columns = ['Rating', 'Year_Month', 'Reviewer_Location']
    df = df.drop(columns=columns, axis = 1)
    
    #separation les données d'entrainnement et de test
    X_train, X_test, y_train, y_test = train_test_split(df.Review_Text, df.Sentiment, test_size=0.25, random_state=42)

    # Initialiser un objet vectorizer
    vectorizer = CountVectorizer()

    #Mettre à jour la valeur de X_train et X_test
    X_train = vectorizer.fit_transform(X_train).todense()
    X_test = vectorizer.transform(X_test).todense()

    #Entrainement du modèle
    clf = LogisticRegression(random_state = 42, C = 5.428675439323859, penalty = 'l2')
    clf.fit(X_train, y_train)

    #prédire la phrase fournit dans le paramètre
    tokenized_comments = vectorizer.transform([phrase])
    pred = clf.predict(tokenized_comments.toarray())
    
    return pred[0]







