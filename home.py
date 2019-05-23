from flask import Flask, render_template, request, redirect, url_for
import requests 
import pandas as pd                          
import io
import re
import nltk
import json
from lxml import html                        
from bs4 import BeautifulSoup                      
from nltk.corpus import stopwords
import tfIdf
import operator
import wildcard
import Positional

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
dicted = {}
wild = []
w = {}
jss = open('TokensWordSort.json')
datas = json.load(jss)
jss.close()
js = open('TokensWord.json')
data = json.load(js)
js.close()
df = pd.read_csv('link1-100.csv')
@app.route('/')
def index ():
  for i in range(0,len(df)): 
    w[i+1] = df['url'][i]
    for j in datas[i]:
      index = all_indices(j,data[i])
      if i != 0:
        if j in dicted:
          dicted[j][i+1] =  index
        else:
          dicted[j] =  i+1
          dicted[j] = {i+1 : index}
      else:
        dicted[j] =  i+1
        dicted[j] = {i+1 : index}
  return render_template("index.html")

@app.route('/result', methods = ['POST', 'GET'])
def result():
    d = []	
    c = 0
    t = []
    lenPo = 1
    tfidfPo = {}
    ni = 1
    np = 1
    wi = " "
    if request.method == "POST":
      tfidf = {}
      s = []
      result = request.args
      global words
      global word
      words = request.form.get("Search")
      word = stop_word(words.lower())
      if words.count('*') != 0:
        n = 1
        wild = wildFunctions()
        return render_template("2result.html ",wi = words,w = wild,len1 = 0,aa = words,n = n)
      else:
        n = 0
        for i in word:
          if i in dicted:
              t.append(i)
              wi = wi+i+" "

        if len(t) != 0:
          if len(word) == len(t):
            po,c = Positional.result(dicted,w,t)
            if len(po) > 0:
              sim = tfIdf.dfFunctions(t,dicted,len(df),data)
              sorted_sim = sorted(sim.items(), key=lambda kv: kv[1] ,reverse=True )
              for v in sorted_sim:
                for i in po:
                  if v[1] > 0 and v[0] == i:
                    tfidfPo[w[v[0]]] = v[1]
            else:
              np = 0
          else:
            np = 0

          sim = tfIdf.dfFunctions(t,dicted,len(df),data)
          sorted_sim = sorted(sim.items(), key=lambda kv: kv[1] ,reverse=True )
          for v in sorted_sim:
            if v[1] > 0:
              tfidf[w[v[0]]] = v[1]
        else:
          ni = 0
          np = 0
          wi = words

      simmPo= tfidfPo.values()
      linkPo = tfidfPo.keys()
      simm= tfidf.values()
      link = tfidf.keys()

    return render_template("2result.html ",wi = wi,len1 = 1,lenPo = len(linkPo),aa = words,simPo = simmPo,linkPo = linkPo,sim = simm,link = link,keys = words,len = len(link), n = n,np = np, ni = ni)
    

def wildFunctions():
  global wild
  for i in word:
    if i.count('*') != 0:
      wild = wildcard.index(dicted,w,i)
      wild.sort()
  return wild

@app.route("/threshold", methods=['POST', 'GET'])
def threshold():
  wil = []
  tfidf = {}
  tfidfPo = {}
  ws = words
  po = []
  to = []
  wor = " "
  np = 1
  if request.method == "POST":
    result = request.args
    wil.append(request.form['wild'])
    for i in word:
      if i.count('*') != 0:
        ww = ws.replace(i,wil[0])
    wordd = stop_word(ww.lower())
    for i in wordd:
          if i in dicted:
              to.append(i)
              wor = wor+i+" "
    if len(wordd) == len(to):
      po,c = Positional.result(dicted,w,to)
    
    sim = tfIdf.dfFunctions(to,dicted,100,data)
    sorted_sim = sorted(sim.items(), key=lambda kv: kv[1] ,reverse=True)
    for v in sorted_sim:
      if v[1] > 0:
        tfidf[w[v[0]]] = v[1]
        
    if len(po) > 0:
      sim = tfIdf.dfFunctions(to,dicted,100,data)
      sorted_sim = sorted(sim.items(), key=lambda kv: kv[1] ,reverse=True)
      for v in sorted_sim:
        for i in po:
          if v[1] > 0 and v[0] == i:
            tfidfPo[w[v[0]]] = v[1]
    else:
      np = 0
    
    simmPo = tfidfPo.values()
    linkPo = tfidfPo.keys()
    simm = tfidf.values()
    link = tfidf.keys()
  return render_template("2result.html ",wi = wor,len1 = 1,aa = wor,w = wild,simPo = simmPo,linkPo = linkPo,lenPo = len(linkPo),sim = simm, link = link,len = len(link),np = np,n = 1)

def stop_word(content):
  words = re.findall("[A-Za-z*]+",content)
  stopWords = set(stopwords.words('english'))
  wordsFiltered = []
  for w in words:
    if w not in stopWords:
      wordsFiltered.append(w)
  return wordsFiltered
 
def duplicates(data):
  data = list(dict.fromkeys(data)) 
  return data
  
def all_indices(value,tokens):
  ind1 =  []
  for index in  range(len(tokens)):
    if  value in tokens[index]:
      ind1.append(index)
  return ind1

if __name__ == "__main__":
    app.run(debug = True,host = "0.0.0.0") 
     