import pickle
import pandas as pd
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import os
  

def classify_text(text, classifier):
    classifier = classifier.replace(" ","_")
    text = [re.sub("[^a-zA-Z0-9]"," ", text)]
    
    with open('./Classifiers/clf_' + classifier + '.pickle', 'rb') as f:
        clf = pickle.load(f)

    with open('./Classifiers/vectorizer_' + classifier + '.pickle', 'rb') as f:
        vectorizer = pickle.load(f)
        
    with open('./Classifiers/oversample_' + classifier + '.pickle', 'rb') as f:
        oversample = pickle.load(f)
    
    test_data_features = vectorizer.transform(text)

    binary_predictions = clf.predict_proba(test_data_features)

    return{classifier:{"probability":binary_predictions[0][1]}}
    
 
def classify_list(text, classifiers):
    """Assign probability that a section of text belongs to one or more classifiers.

       Args:
           text: the text to be classified
           classifiers: a list of classifiers 
       Returns:
           a dictionary containing each classifier (key) and the probabilty 
           that the text should be included in this classifier (value)
       """
    class_predictions = {}
    
    for c in classifiers:
        class_predictions.update(classify_text(text, c))
    
    return {"class_predictions":class_predictions}

def get_classifiers():
    classifiers = []
    for file in os.listdir("./Classifiers"):
        if file.startswith("clf_"):
            classifiers.append(file[4:][:-7])
            
    return classifiers

def get_features(classifier):
    with open('./Classifiers/clf_' + classifier + '.pickle', 'rb') as f:
        clf = pickle.load(f)

    with open('./Classifiers/vectorizer_' + classifier + '.pickle', 'rb') as f:
        vectorizer = pickle.load(f)     
    
    features = dict(zip(vectorizer.get_feature_names(), clf.feature_importances_))
    
    features = {key:val for key, val in features.items() if val > 0}
    
    return features

def get_oversample(classifier):
    with open('./Classifiers/oversample_' + classifier + '.pickle', 'rb') as f:
        oversample = pickle.load(f)
        
    return oversample
        
        
def adjust_oversample(oversampled_fraction, original_fraction, scoring_result):
    return (1/(1+(1/original_fraction-1)/(1/oversampled_fraction-1)*(1/scoring_result-1)))

def delete_classifier(name):
    os.remove("./classifiers/clf_" + name + ".pickle")
    os.remove("./classifiers/oversample_" + name + ".pickle")
    os.remove("./classifiers/vectorizer_" + name + ".pickle")
    return {'classsifier': name}