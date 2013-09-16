ratings_list=list(open('recsys-data-ratings.csv'))
users_list=list(open('recsys-data-users.csv'))
movies_list=list(open('recsys-data-movie-titles.csv'))

users=set()
movies=set()

ratings=dict()

#for row in users_list: users[row.split(',')[0]]=row.split(',')[1]
#for row in movies_list: movies[row.split(',')[0]]=row.split(',')[1]

for row in ratings_list:
    u = int(row.split(',')[0])
    m = int(row.split(',')[1])
    r = float(row.split(',')[2])
    users.add(u)
    movies.add(m) 
    ratings[(u,m)]=r


x_task=[453,161,602]
#x_task=[11,121,8587]


for x in x_task:
    r1=[]
    r2=[]
    
    xx=len([ 1 for u in users if (u,x) in ratings])
    _xx = len([ 1 for u in users if (u,x) not in ratings])
    
    
    xy = { y:len([ 1 for u in users if (u,y) in ratings and (u,x) in ratings]) for y in movies}
    _xy = { y:len([ 1 for u in users if (u,y) in ratings and (u,x) not in ratings]) for y in movies}
    
    dict1 = { y:((xy[y] if xy[y]!=0 else 1)/(xx if xx!=0 else 1)) for y in movies }
    dict2 = { y:(((xy[y] if xy[y]!=0 else 1)/(xx if xx !=0 else 1))/((_xy[y]if _xy[y]!=0 else 1)/(_xx if _xx!=0 else 1))) for y in movies }
    
    r_dict1 = {dict1[k]:k for k in  dict1.keys()}
    r_dict2 = {dict2[k]:k for k in  dict2.keys()}
    
    s_dict1 = [(r_dict1[k],round(k,2)) for k in reversed(sorted(r_dict1.keys()))]
    s_dict2 = [(r_dict2[k],round(k,2)) for k in reversed(sorted(r_dict2.keys()))]
    
    r1.append(x)
    r2.append(x)
    for i in range(1,6):
        r1+= s_dict1[i];
        r2+=s_dict2[i];
        
    print(r1)
    print(r2)