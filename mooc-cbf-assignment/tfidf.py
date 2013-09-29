tags_file=open('data/movie-tags.csv')
titles_file=open('data/movie-titles.csv')
ratings_file=open('data/ratings.csv',errors='ignore')
user_file=open('data/users.csv')

#tags={ (row.split(',')[1],row.split(',')[0]) : (tags[(row.split(',')[1],row.split(',')[0])]+1 if (row.split(',')[1],row.split(',')[0]) in tags else 1) for row in list(tags_file)}

tags=dict()
for row in ratings_file:
    r=row.split(',')
    if r[1] in tags:
        d_t = tags[r[1]]
        if r[0] in d_t:
            d_t[r[0]]+=1
        else:
            d_t[r[0]] = 1
        tags[r[1]]= d_t
    else:
        tags[r[1]] = {r[0]:1}

print(tags)



                       
                       
                                           

    
