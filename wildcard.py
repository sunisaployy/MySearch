import fnmatch
def index(dicted,w,word):
    t = []
    #for i in word:
    fil = fnmatch.filter(dicted.keys(),word)
    for j in fil:
        if j in dicted: 
            t.append(j)
    return t

# def wild(dicted,w,word):
#     d = []
#     dd = []
#     c = 0
#     print(word)
#     for i in word:
#         for k in dicted[i]:
#             c += 1
#             d.append(w[k])
#             #dd.append(k)

#     return d