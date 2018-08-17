## get the number of observations for each study
## select studies.name, count(studies.name) from studies, entities, observations where studies.id = observations.study_id and entities.id = observations.entity_id group by (studies.name) order by count(studies.name) ASC;

import json
import re
import pandas as pd
import MySQLdb
import config

f = open("__data_export.json")
data = json.load(f)

keywords = set()
for d in data.keys():
    for k in data[d]['keywords']:
        keywords.add(k)

keys = data['NCT01778439'].keys()

studies = data.keys()

data_0 = data['NCT01778439']

data_text = ""
for k in keys:
    if type(data_0[k]) is list or data_0[k] is None:
        continue
    else:
        data_text += str(data_0[k]) + ' '
    data_text = re.sub("[^a-zA-Z0-9]"," ", data_text)
    data_text = ' '.join(data_text.split())

#data_text

i = 0
keyword_col = []
unique_keywords = set()
id_col = []
data_text_col = []
for d in data.keys():
    if i > 100000:
        break
    else:
        i += 1
        name = d
        keywords = []
        for k in data[d]['keywords']:
            word = re.sub("[^a-zA-Z0-9/s]"," ", k).strip().lower()
            word = word.replace(" ", "_")
            keywords.append(word)
            unique_keywords.add(word)
        data_text = ""
        for k in data[d].keys():
            if type(data[d][k]) is list or data[d][k] is None:
                continue
            else:
                data_text += str(data[d][k]) + ' '
        data_text =  re.sub('<[^<]+?>', '', data_text)
        data_text = re.sub("[^a-zA-Z0-9]"," ", data_text)
        data_text = ' '.join(data_text.split())
        
        id_col.append(name)
        data_text_col.append(data_text)
        keyword_col.append(keywords)

#print(unique_keywords)

db=MySQLdb.connect(host=config.host,user=config.user,
                      passwd=config.passwd,db=config.db)

c=db.cursor()

for k in unique_keywords:
    q = "insert into studies (name, is_train, created_at, updated_at) values ('" + k + "', 1, now(), now())"
    c.execute(q)
    db.commit()

for i in range(len(id_col)):
    q = "insert into entities (item, created_at, updated_at) values ('" + data_text_col[i] + "', now(), now())"
    c.execute(q)
    db.commit()
    entity_id = c.lastrowid

    for k in keyword_col[i]:
        is_match = 1
        
        q = "select id from studies where name = '" + k + "'"
        #print(q)
        c.execute(q)
        for r in c.fetchall():
            study_id = r[0]
        
        q = "insert into observations (study_id, entity_id, is_match, created_at, updated_at) values ("
        q += str(study_id) + "," + str(entity_id) + ", " + str(is_match) + ", now(), now())"
    
        #print(q)
   
        c.execute(q)
        db.commit()

c.close()
db.close()
del c
del db