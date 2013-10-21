from mat import *
from vec import *
from matutil import *
from vecutil import *
import matutil

matrix = list(open('recsys-data-sample-rating-matrix.csv'))


movies = set()

ratings = dict()

header = matrix[0];
tokens = header.split(',')

users = [float(tokens[i].replace('\"','')) for i in range(1,len(tokens)) ]

for r in range(1,len(matrix)):
    row = matrix[r]
    tokens = row.split(',')
    movies.add(tokens[0].replace('\"',''));
    for t in range(1,len(tokens)):
        tok =tokens[t]
        if tok != '' and tok!='\n':
            ratings[users[t-1]]= float(tokens[t])




ratings_mat = Mat([users,movies], ratings)
normalized = dict()
#normalize
for (u,user_vec) in matutil.mat2coldict(ratings_mat).items():
    user_mean = sum(user_vec.f.values())/len(user_vec.f.values())
    normalized[u] = Vec(user_vec.D,{d:(user_vec[d]-user_mean) for d in user_vec.D} )

normalized_mat = coldict2mat(normalized)

correlation = dict()
for  (u,u_vec) in matutil.mat2coldict(normalized_mat).items():
    correlation[u] = {v:u_vec*v_vec for (v,v_vec) in matutil.mat2coldict(normalized_mat).items() }
    
print(correlation[3712,3712])
print(correlation[3712,2824])
print(correlation[3712,3867])
print(correlation[3712,5062])
print(correlation[3712,442])
print(correlation[3712,3853])