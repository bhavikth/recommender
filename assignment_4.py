from math import sqrt
from copyreg import pickle

matrix = list(open('recsys-data-sample-rating-matrix.csv'))

def transform():
    movies = set()
    
    ratings_movie = dict()
    
    header = matrix[0];
    tokens = header.split(',')
    
    users = [int(tokens[i].replace('\"','')) for i in range(1,len(tokens)) ]
    ratings_user = {user:dict() for user in users}
    
    for r in range(1,len(matrix)):
        row = matrix[r]
        tokens = row.split(',')
        movie = int(tokens[0].replace('\"','').split(':')[0])
        movies.add(movie);
        ratings_movie[movie]=dict()
        for t in range(1,len(tokens)):
            tok =tokens[t]
            if tok != '' and tok!='\n':
                ratings_movie[movie][users[t-1]]= float(tok)
                ratings_user[users[t-1]][movie] = float(tok)
                yield((users[t-1],movie),tok)
    
def printFile():
    ercfile = open('recfile.csv','w');
    toks = list(transform())
    for t in toks:
        line = str(t[0][0])+","+str(t[0][1])+","+str(t[1])+"\n"
        ercfile.write(line)
    ercfile.close()    
                

def correlate():
    movies = set()
    
    ratings_movie = dict()
    
    header = matrix[0];
    tokens = header.split(',')
    
    users = [int(tokens[i].replace('\"','')) for i in range(1,len(tokens)) ]
    ratings_user = {user:dict() for user in users}
    
    for r in range(1,len(matrix)):
        row = matrix[r]
        tokens = row.split(',')
        movie = int(tokens[0].replace('\"','').split(':')[0])
        movies.add(movie);
        ratings_movie[movie]=dict()
        for t in range(1,len(tokens)):
            tok =tokens[t]
            if tok != '' and tok!='\n':
                ratings_movie[movie][users[t-1]]= float(tok)
                ratings_user[users[t-1]][movie] = float(tok)
    
    
    
    norm_user_rating = dict()
    for user in users:
        allmoviesofuser = ratings_user[user].values()
        user_mean = sum(allmoviesofuser)/len(allmoviesofuser)
        norm_user_rating[user] = dict()
        for movie in ratings_user[user]:
            norm_user_rating[user][movie] = ratings_user[user][movie] - user_mean
    
    correlation = dict()
    
    for u in users:
        uu = sqrt(sum([i**2 for i in norm_user_rating[u].values()]))
        correlation[u] = dict()
        for v in users:
            vv = sqrt(sum([i**2 for i in norm_user_rating[v].values()]))
            uv = sum([ norm_user_rating[u][m]* norm_user_rating[v][m] for m in movies if m in norm_user_rating[u] and m in norm_user_rating[v]])
            correlation[u][v] = uv/(uu*vv)
    return correlation
        
c=correlate()

print(str(c[1648][5136])+"=0.40298")
print(str(c[918 ][2824 ])+"=-0.31706")        


def printExcelTgts():
    for i in range(0,25):
        c=chr(ord('B')+i)
        str='=CORREL(Sheet1!$'+c+'$2:Sheet1!$'+c+'$101,Sheet1!B2:Sheet1!B101)'
        print(str)
    
    
printExcelTgts()
