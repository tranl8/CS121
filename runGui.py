from tkinter import *
import tkinter.messagebox
import searchIndex
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize

app = Tk()
app.title("SearchUCI")
app.geometry("1000x600+200+200")
lmtzr = WordNetLemmatizer()
# Code to add widgets will go here...

def searchQuery():
    # search = lmtzr.lemmatize(query).lower()
    # print(search)
    # search = re.sub(r'[^a-zA-Z]', " ", search)
    # terms = word_tokenize(search)
    for i in range(10):
        lb.delete(i, END)
    search = lmtzr.lemmatize(query.get()).lower()
    search = re.sub(r'[^a-zA-Z]', " ", search)
    terms = word_tokenize(search)
    lb.pack()
    if len(terms) > 1:
        try:
            result = searchIndex.run(terms)
            for count, i in enumerate(result):
                lb.insert(END, str(count + 1) + " : " + i['url'])
        except:
            lb.insert(END, "No results found.")
    else:
        try:
            result = searchIndex.run_single_search(terms[0])
            for count, id in enumerate(result):
                lb.insert(END, str(count + 1) + " : " + id['url'])
        except:
            lb.insert(END, "No results found.")


queryBox = StringVar(None)
query = Entry(app, textvariable="query")
query.pack()

button1 = Button(app, text="Search!", width=20, command=searchQuery)
button1.pack()

lb = Listbox(app, height=10, width=800)

app.mainloop()
