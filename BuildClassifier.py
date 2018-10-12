# to run from command line
#  python -c 'from BuildClassifier import build_classifier; build_classifier(<classifier_name>, <classifier_type)'

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import pandas as pd
import pickle
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())
import MySQLdb
import config
import traceback

def build_all():
    
    print("building")
    #for file in glob.glob('./data/*csv'):
    #    print(file[7:-4])
    #    build_classifier(file[7:-4])

    classifier_types = ["RandomForest", "MLP", "MultinomialNB", "LogisticRegression"]
    

    db=MySQLdb.connect(host=config.host,user=config.user,
                      passwd=config.passwd,db=config.db)

    c=db.cursor()

    #q = "select name from studies"

    for classifier_type in classifier_types:

        q = "select studies.name, count(studies.name) from studies, entities, observations \
        where studies.id = observations.study_id and entities.id = observations.entity_id \
        group by (studies.name) HAVING count(studies.name) > 1 order by count(studies.name) ASC;"

        c.execute(q)
    
        for r in c.fetchall():
            build_classifier(r[0], classifier_type)

def build_classifier(classifier_name, classifier_type):

    try:

        db=MySQLdb.connect(host=config.host,user=config.user,
                      passwd=config.passwd,db=config.db)

        c=db.cursor()

        # total number of records, used for calculating oversample ratio
        q = "select count(1) from entities"
        c.execute(q)
    
        total = c.fetchone()[0]

        q = "select entities.id, entities.item \
            from entities, observations, studies \
            where entities.id = observations.entity_id \
            and studies.id = observations.study_id \
            and name = '" + classifier_name + "'"

        c.execute(q)

        names = ["id", "text", "category"]

        ids = []
        texts = []
        categories = []

        for r in c.fetchall():
            ids.append(r[0])
            texts.append(r[1])
            categories.append(1)

        # if you want to use a 50-50 balance
        count = len(ids)
    
        # balance it out with non-observations, 
    
        q = "select distinct entities.id, entities.item \
            from entities, observations, studies \
            where entities.id = observations.entity_id \
            and studies.id = observations.study_id \
            and name <> '" + classifier_name + "' ORDER BY RAND() LIMIT " + str(count)

        print(q)

        c.execute(q)

        for r in c.fetchall():
            ids.append(r[0])
            texts.append(r[1])
            categories.append(0)

        # randomize and join the data sets, limted to the size of the smaller one, then concat
        #pos = sqldf("SELECT * FROM train WHERE category = 1 ORDER BY RANDOM() LIMIT " + str(count))
        #neg = sqldf("SELECT * FROM train WHERE category = 0 ORDER BY RANDOM() LIMIT " + str(count))
        #train = pd.concat([pos, neg])

        oversample = {classifier_name:(count / total)}
        print(oversample)
    
        train = pd.DataFrame({"id":ids, "text":texts, "category":categories})

        print(train)

        vectorizer = CountVectorizer()

        vectorizer = CountVectorizer(analyzer='word', binary=False, decode_error='strict',
                encoding='utf-8', input='content',
                lowercase=True, max_df=1.0, max_features=10000, min_df=1,
                ngram_range=(1, 2), preprocessor=None, stop_words="english",
                strip_accents=None, token_pattern='(?u)\\b\\w\\w+\\b',
                tokenizer=None, vocabulary=None)

        train_data_features = vectorizer.fit_transform(train["text"])

        if classifier_type == "RandomForest":
            clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                    max_depth=None, max_features='auto', max_leaf_nodes=None,
                    min_impurity_decrease=0.0, min_impurity_split=None,
                    min_samples_leaf=1, min_samples_split=2,
                    min_weight_fraction_leaf=0.0, n_estimators=500, n_jobs=1,
                    oob_score=True, random_state=None, verbose=0,
                    warm_start=False)
                    
        elif classifier_type == "MLP":
            clf = MLPClassifier()
        
        elif classifier_type == "MultinomialNB":
            clf = MultinomialNB()
            
        elif classifier_type == "LogisticRegression":
            clf = LogisticRegression()
            
        elif classifier_type == "SVC":
            clf = SVC()

        else:
            print("error - no matching classifier")
            exit(-1)

        clf.fit( train_data_features, train["category"] )    

        with open('./Classifiers/clf_' + classifier_name + '_' + classifier_type + '.pickle', 'wb') as f:
            pickle.dump(clf, f, pickle.HIGHEST_PROTOCOL)

        with open('./Classifiers/vectorizer_' + classifier_name + '_' + classifier_type + '.pickle', 'wb') as f:
            pickle.dump(vectorizer, f, pickle.HIGHEST_PROTOCOL)

        with open('./Classifiers/oversample_' + classifier_name + '_' + classifier_type + '.pickle', 'wb') as f:
            pickle.dump(oversample, f, pickle.HIGHEST_PROTOCOL)
        
    except:
        print("*** error ***")
        print(classifier_name)
        print(traceback.format_exc())
        
if __name__ == '__main__':
    build_all()