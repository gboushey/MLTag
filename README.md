Overview:

App to create a binary classification model, and made the classification model available as a web service.

Usage:

import file

place import file in import
currently named dash-import.csv
must have columns:
id,name,abstract,methods,tags,text,category
tags is a multi value comma delimited column
(ie., store mutiple tags here, separate with commas)

to prepare a single model
run 
% python PrepareDataFile.py <importfilename> <tagname>
ex:
% python PrepareDataFile.py dash-import.csv 'Carbon Dates'
Note - you can have spaces in your tag names, though probably better to avoid them
Note - <tagname> is a tag that shows up in the comma delimited tags column

to prepare all models
run
% python CreateClassifiers.py <importfilename>

to build the classifier for a single model
run
% python BuildModel <tag_name>
note that the tag must have been included and PrepareDataFile needs to have been run for this tag

to process all the tags and build all the models
run
% python CreateClassifiers.py <importfilename>
this could take a while

to start the service:
% python ClassifyService

API

in dev, these are all set to run from http://localhost:8080

/classify
Takes two parameters
text (the text to classify)
classifier (the classifier built for a particular tag)
output - the probabilty, absolute and adjusted for oversampling, that the text would be propery classified under the tag
example: /classify?tag=bacteria&text=this+is+a+study+of+bacteria+in+the+stomach+microbiome

/classify_multiple
takes two parameters
text (the text top classify)
classifiers (a list of classifiers to apply to the text)
output - a list of probabilities, absolute and adjusted for oversampling, that the text belongs in each tag in the classifier list

/classifiers
returns all available classifiers (corresponding to tags) available in the system

/features
parameters
classifier
output - a list of words/phrases (single and 2-gram) that are used to determine tag probability, along with the estimate of value in making the classifiction (as percentage)

/rate_this
a form for rating text for a single classifier

/rate_multiple
a form for rating text for multiple classifiers

