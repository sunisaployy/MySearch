
def result(dicted,w,word):
  d = []
  t = []
  c = 0
  for i in word:
    if i in dicted: 
      t.append(i)
        
  if len(word) == 1 and len(t) == 1:
    c += 1
    for k in dicted[t[0]]:
      c += 1
      d.append(k)
  elif len(t)==len(word) and len(t) > 1:
    c += 1
    inter,c = intersec(t , dicted,c)
    for j in inter:
      c += 1
      w1 = t[0]
      for i in range(0,len(dicted[w1][j])):
        c += 1
        p,c = Positional( j, dicted , t ,dicted[w1][j][i],c)
        if  p == len(t)-1:
          c += 1
          d.append(j)   
    
  return set(d),c

def intersec(search,dicts,c):
  intersect = {}
  
  n = 0
  for i in search:
    c += 1
    if i in dicts.keys():
      c += 1
      lists = []
      for j in dicts[i]:
        c += 1
        lists.append(j)
        s = set(lists)
      intersect[n] = s
      n += 1
    else:
      c += 1
      n = 0
      break
      
  first = intersect[0]
  for i in intersect.keys():
    c += 1
    s1 = first.intersection(intersect[i])
    first = s1
    s2 = first
    
  return list(s2),c

def  Positional(page , d  , w , index,co):
  c = 0
  word1 = w[0]
  num = len(w)
  for i in range(1,num):
    co += 1
    word = w[i]
    if index+i in d[word][page]:
      co += 1
      c += 1
    else:
      co += 1
      continue
        
  return c,co
 
     