from math import log2

tags_file=open('data/movie-tags.csv')
titles_file=open('data/movie-titles.csv')
ratings_file=open('data/ratings.csv')
user_file=open('data/users.csv')


tags_movies=dict()
movies_tag=dict()

def get_rows(file):
    for row in file:
        rows = row.split('#')
        for r in rows:
            if ',' in r:
                yield r



for row in get_rows(tags_file):
    r=row.split(',')
    tag = r[1]
    movieId = int(r[0])
    if movieId in movies_tag:
        if tag in movies_tag[movieId]:
            movies_tag[movieId][tag]+=1
        else:
            movies_tag[movieId][tag] = 1
    else:
        movies_tag[movieId] = {tag:1}
        
    if tag in tags_movies:
        if movieId in tags_movies[tag]:
            tags_movies[tag][movieId]+=1
        else:
            tags_movies[tag][movieId]=1
    else:
        tags_movies[tag] = {movieId:1}

print(tags_movies.keys())

user_ratings=dict()
movie_rating = dict()

for row in ratings_file:
    r=row.split(',')
    userId=int(r[0])
    movieId=int(r[1])
    rating = float(r[2])
    if userId in user_ratings:
        user_ratings[userId][movieId] = rating
    else:
        user_ratings[userId]={movieId:rating}  
    
    if movieId in movie_rating:
        if rating in movie_rating[movieId]:
            movie_rating[movieId][rating] +=1
        else:
            movie_rating[movieId][rating] = 1
    else:
        movie_rating[movieId] = {rating:1}




                       
                       
                                           

    
 