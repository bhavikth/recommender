from math import log2

tags_file=open('data/movie-tags.csv')
titles_file=open('data/movie-titles.csv')
ratings_file=open('data/ratings.csv')
user_file=open('data/users.csv')


tags_movies=dict()
movies_tags=dict()

def get_rows(file):
    for row in file:
        rows = row.split('#')
        for r in rows:
            if ',' in r:
                yield r



for row in get_rows(tags_file):
    r=row.split(',')
    tag = r[1].upper()
    movieId = int(r[0])
    if movieId in movies_tags:
        if tag in movies_tags[movieId]:
            movies_tags[movieId][tag]+=1
        else:
            movies_tags[movieId][tag] = 1
    else:
        movies_tags[movieId] = {tag:1}
        
    if tag in tags_movies:
        if movieId in tags_movies[tag]:
            tags_movies[tag][movieId]+=1
        else:
            tags_movies[tag][movieId]=1
    else:
        tags_movies[tag] = {movieId:1}


tag = 'DISNEY'
tfidf_tag = {tag:{movie: tags_movies[tag][movie] * log2(sum(tags_movies[tag].values()) / (tags_movies[tag][movie])) for movie in tags_movies[tag]} for tag in tags_movies }

tfidf_movie = {movie:{tag: tags_movies[tag][movie] * log2(sum(tags_movies[tag].values()) / (tags_movies[tag][movie])) for tag in movies_tags[movie]} for movie in movies_tags }
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




                       
                       
                                           

    
 
