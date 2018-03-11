from nltk.stem.wordnet import WordNetLemmatizer
from pymongo import MongoClient
from nltk.tokenize import word_tokenize
import re

client = MongoClient()
db_terms = client['SearchEngine']['terms']
db_bookkeeping = client['SearchEngine']['bookkeeping']
lmtzr = WordNetLemmatizer()


def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

search = lmtzr.lemmatize(raw_input("What would you like to search?")).lower()
print(search)
search = search.lower()
search = re.sub(r'[^a-zA-Z]', " ", search)
terms = word_tokenize(search)
merge_id = []
union_id=[]

for term in terms:
    term_result = db_terms.find_one( {"term" : term} )
    if term_result != None:
        id = []
        results = term_result['found in']
        for i in results:
            id.append(i[0])
        union_id.append(id)
merge_id = intersect(union_id[0], union_id[1])
print merge_id


# results_sorted = sorted(results, key=lambda x:x[2], reverse=True)
counter = 0
while counter < 10:
    # result = results_sorted[counter]
    # bk_path= result[0]
    # count = result[1]
    # tf_idf= result[2]
    # print str(counter + 1) + "[" + str(tf_idf) + "]: " + db_bookkeeping.find_one(
    #     {
    #     'bk_path':bk_path
    #     }
    # )['url']
    # counter += 1
    print db_bookkeeping.find_one(
        {
        'bk_path':merge_id[counter]
        }
    )['url']
    counter +=1

#print(term_result)