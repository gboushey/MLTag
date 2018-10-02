from bottle import route, run, request, response, template
from ClassifyMethods import *
from BuildClassifier import *

@route('/classify')
def classify():
    
    text = request.query.text
    classifier = request.query.classifier
    classifier_type = request.query.classifier_type
    
    return classify_text(text, classifier, classifier_type)
        
@route('/classify_multiple')
def classify_multiple():
    text = request.query.text
    classifier_type = request.query.classifier_type
    classifiers = request.GET.getall('classifiers')
    if not classifiers:
        classifiers = get_classifiers()
        
    return classify_list(text, classifiers)
   
@route('/classifiers')
def classifiers():
    return {'classifiers':get_classifiers()}
    
@route('/features')
def features():
    classifier = request.query.classifier
    classifier = classifier.replace(" ","_")
    
    return get_features(classifier)

@route('/oversample')
def features():
    classifier = request.query.classifier
    classifier = classifier.replace(" ","_")
    
    return get_oversample(classifier)

@route('/rate')
def rate_this():
    classifiers = get_classifiers()
    return template('rate', classifiers=classifiers)
    
@route('/rate_multiple')
def rate_multiple():
    classifiers = get_classifiers()
    return template('rate_multiple', classifiers=classifiers)

@route('/delete')
def delete():
    classifier = request.query.classifier
    return delete_classifier(classifier)

@route('/generate_classifier')
def generate_classifier():
    classifier = request.query.classifier
    classifier_type = request.query.classifier_type
    build_classifier(classifier, classifier_type)
    return {'classifier': classifier}
    
@route('/generate_all_classifiers')
def generate_all_classifiers():
    build_all()
    return {'classifier': 'all'}

run(host='localhost', port=8080, debug=True)
