from nltk.stem.wordnet import WordNetLemmatizer
from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from collections import defaultdict
import re, math

client = MongoClient()
db_terms = client['SearchEngine']['terms']
db_bookkeeping = client['SearchEngine']['bookkeeping']
lmtzr = WordNetLemmatizer()
score_doc = defaultdict(list)
id_list = defaultdict(list)

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def dot_product(lista, listb):
    result = 0.0
    for i in range (len(lista)):
        result += lista[i] * listb[i]
    return result

search = lmtzr.lemmatize(raw_input("What would you like to search?")).lower()
print(search)
search = search.lower()
search = re.sub(r'[^a-zA-Z]', " ", search)
terms = word_tokenize(search)
merge_id = []
union_id=[]
term_result = []
scoreQuery = 0.0
weight_query = []
similarity = defaultdict(list)
for i, term in enumerate(terms):
    term_result.append(db_terms.find_one( {"term" : term} ))

    if term_result[i] != None:
        id = []
        results = term_result[i]['found in']
        idf = term_result[i]['idf']
        for i in results:
            id.append(i[0])
        union_id.append(id)
        weight_query.append(round(term.count(term) /float(len(terms)) * idf,3))
print weight_query
for i in weight_query:
    scoreQuery += i ** 2
scoreQuery = math.sqrt(scoreQuery)
merge_id = intersect(union_id[0], union_id[1])

for i, term in enumerate(terms):
    results = term_result[i]['found in']
    for i in results:
        if i[0] in merge_id:

            id_list[i[0]].append(i[2])
for id, posting in id_list.iteritems():
    score = 0.0
    for i in posting:
        score += i ** 2
    score = math.sqrt(score)
    score_doc[id].append(score)


for id in merge_id:
    weight = id_list[id]
    dot = dot_product(weight_query,weight)
    similarity[id] = [dot / scoreQuery * score_doc[id][0]]

print id_list
print("")
print merge_id
print("")
print score_doc
print similarity # sort this dictionary and print out the url


# results_sorted = sorted(results, key=lambda x:x[2], reverse=True)
# counter = 0
# while counter < 10:
#     # result = results_sorted[counter]
#     # bk_path= result[0]
#     # count = result[1]
#     # tf_idf= result[2]
#     # print str(counter + 1) + "[" + str(tf_idf) + "]: " + db_bookkeeping.find_one(
#     #     {
#     #     'bk_path':bk_path
#     #     }
#     # )['url']
#     # counter += 1
#     print db_bookkeeping.find_one(
#         {
#         'bk_path':merge_id[counter]
#         }
#     )['url']
#     counter +=1

#print(term_result)
