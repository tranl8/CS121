from __future__ import division
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import math
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os, re
import json
import io, gc

client = MongoClient()
db_terms = client['SearchEngine']['terms']
db_bookkeeping = client['SearchEngine']['bookkeeping']


corpus_files = {}
docid = {}
numdoc = []
index = defaultdict(list)

stop_words = set(stopwords.words("english"))

bookkeeping = {}
lmtzr = WordNetLemmatizer()
index = defaultdict(list)  # the inverted index


def init_bookkeeping():
    global bookkeeping
    with open('WEBPAGES_RAW/bookkeeping.json', 'r') as f:
        bookkeeping = json.load(f)
        for dirCombo in bookkeeping:
            db_bookkeeping.insert({
                'bk_path': dirCombo,
                'url' : bookkeeping[dirCombo]
            })


def readFile():
    courpusCounter = 0
    topdir = 'WEBPAGES_RAW'
    for dirpath, dirnames, files in os.walk(topdir):
        for dir in dirnames:

            path = os.path.join(dirpath, dir)
            for file in os.listdir(path):
                path_file = os.path.join(path, file)
                docid[courpusCounter] = path_file[13:]
                corpus_files[courpusCounter] = path_file
                courpusCounter += 1
    print docid

def term_tokenize():
    global numdoc
    count = 0
    for file in corpus_files:
        termdictPage ={}
        # f = io.open(corpus_files[file], 'r')
        f = io.open(corpus_files[file], 'r', encoding='utf-8')
        # f = io.open('WEBPAGES_RAW/39/372', 'r', encoding='utf-8')
        # document = f.read()
        document = f.read().encode('utf-8')
        f.close()
        if (bool(BeautifulSoup(document,"html.parser").find())):
            numdoc.append(1)
            soup = BeautifulSoup(document, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head'])]
            visible_text = soup.getText()

            print corpus_files[file]
            # print visible_text
            visible_text = re.sub(r'[^a-zA-Z]', " ", visible_text)
            terms = word_tokenize(visible_text)
            filtered_term = [lmtzr.lemmatize(w).lower() for w in terms if not w in stop_words]
            id = docid[count]  # Doc id (FOLDER\\ID)
            id = id.replace('\\', '/')
            numte = len(filtered_term)
            for term in filtered_term:
                term_count =  filtered_term.count(term)
                weight_term_frequency = 1 + math.log(term_count,10)
                termdictPage[term] = [id, term_count,weight_term_frequency]
            for termpage, postingpage in termdictPage.iteritems():
                index[termpage].append(postingpage)
        else:
            print("none")
        count = count + 1

def export_to_mongo():
    diclen = len(numdoc)
    print diclen
    for term, count in index.iteritems():
        doclen = len(index[term])
        idf = math.log(diclen/doclen,10)
        for id in count:
            rank = round(id[2] * idf,5)
            id[2] = rank
        db_terms.insert({
                        'term': term,
                        'found in': count})

        # for id in count:
        #
        #     rank = round(id[2] * idf,5)
        #     id.append(rank)
        #     db_terms.find_one({
        #         'term' : term,
        #         'docid': id[0],
        #         'term_count': id[1],
        #         'tf' : id[2],
        #         'tf-idf': id[3]
        # })
def main():
    # init_bookkeeping()
    readFile()
    term_tokenize()
    export_to_mongo()



if __name__ == "__main__":
 main()
