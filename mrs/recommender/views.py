# import os
from http.client import ResponseNotReady
import random
from django.http import HttpResponse, HttpResponseRedirect
# import numpy as np
# import pickle
# import pandas as pd

from django.shortcuts import render
from pathlib import Path
from django.contrib import messages
from .models import MovieRecommender
from .models import CollabarativeMovieRecommender, MatrixMovieRecommender
from django.contrib.auth.models import User

import requests

BASE_DIR = Path(__file__).resolve().parent.parent


""" Database Modelling """


# # 1. content based db modelling...

# # loading pickle files..
# movies_dict = pickle.load(open( os.path.join(BASE_DIR, "movies_dict.pkl"), 'rb'))
# movies = pd.DataFrame(movies_dict)

# similarity_matrix = pickle.load(open( os.path.join(BASE_DIR, "similarity_matrix.pkl"), 'rb'))

con_movie_ids = [19995, 285, 206647, 49026, 49529, 559, 38757, 99861, 767, 209112, 1452, 10764, 58, 57201, 49521, 2454, 24428, 1865, 41154, 122917, 1930, 20662, 57158, 2268, 254, 597, 271110, 44833, 12155, 36668, 62211, 8373, 91314, 68728, 102382, 20526, 49013, 44912, 10193, 534, 168259, 72190, 127585, 54138, 81005, 64682, 9543, 68726, 38356, 217, 105864, 62177, 188927, 10681, 674, 8960, 6479, 118, 2062, 272, 10527, 18360, 2080, 605, 109445, 604, 76338, 76341, 13448, 10195, 13053, 19585, 57165, 62213, 177677, 7978, 5559, 49444, 10196, 956,  82703, 652, 80321, 140300, 56292, 81188, 13475, 557, 82702, 205584, 10048, 13183, 944, 1927, 72559, 7364, 2114, 1771, 36643, 8619, 50620, 65759, 1724, 267935, 281957, 77950, 44896, 270946, 2503, 9502, 102899, 101299, 228161, 74, 8961, 417859, 27576, 86834, 17578, 673, 6972, 82700, 10567, 181533, 38055, 671, 49524, 22]


# storing in model MovieRecommender
# primary key : current movie id, and 
# containing best 5 recommended movies id corresponding to it
# def generateMovieRecommender(request):

#     for x in similarity_matrix :
#         distances = sorted(list(enumerate(x)), reverse=True, key = lambda z : z[1])[:6]

#         movie_ids= []
#         for x in distances :
#             movie = movies.iloc[x[0]]
#             movie_ids.append(movie.movie_id)

#         recommender = MovieRecommender(movieId = movie_ids[0], movie1 = movie_ids[1], movie2 = movie_ids[2], movie3 = movie_ids[3], movie4 = movie_ids[4], movie5 = movie_ids[5])
#         recommender.save()

#     return HttpResponse("Content Based Movie Recommender Model is Created.")



# # 2. collabarative database modelling....

# coll_movies_csv = pd.read_csv(os.path.join(BASE_DIR, "collaborative.csv"))

# def generateCollModel(request):

#     for i in range(0, 608):

#         if i == 576 :
#             continue;

#         data = [int(x) for x in list(coll_movies_csv.iloc[i])]
#         ids = [i]
#         ids.extend(data)

#         recommender = CollabarativeMovieRecommender(userId = ids[0], movie1 = ids[1], movie2 = ids[2], movie3 = ids[3], movie4 = ids[4], movie5 = ids[5], movie6 = ids[6])
#         recommender.save()

#     return HttpResponse("Collabarative Base Movie Recommender model is created.");


# # 3.  matrix based factorization..

# matrix_movies_csv = pd.read_csv(os.path.join(BASE_DIR, "matrix_factorisation.csv"))

# def generateMatrixModel(request):

#     for i in range(0, 610):
#         data = [int(x) for x in list(matrix_movies_csv.iloc[i])]
#         ids = [i]
#         ids.extend(data)
    
#         #creating db model.
#         recommender = MatrixMovieRecommender(userId = ids[0], movie1 = ids[1], movie2 = ids[2], movie3 = ids[3], movie4 = ids[4], movie5 = ids[5])
#         recommender.save()

#     return HttpResponse("Matrix Movie Recommender is created")




# banner page
def bannerPage(request):
    return render(request, 'banner.html')

def getMovieRecommendData( responseData ):
    
    data = {}

    try :
        data['id'] = responseData['id']
        data['title'] = responseData['title']
        data['votes'] = responseData['vote_count']
        data['rating'] = responseData['vote_average']
        data['poster_path'] = "https://image.tmdb.org/t/p/w500/" + responseData['poster_path']
    except :
        return None
    
    return data


# home page ... 
def homePage(request):

    data = []
    for movie_id in random.sample(con_movie_ids, 12):
        res = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=73b7b94a31ab039b04bad943834342bd")
        responseData = res.json()
        
        temp = getMovieRecommendData(responseData)
        if temp != None:
            data.append(temp)

    return render(request, "home.html", {'data' : data})


# about page...
def aboutPage(request):
    return render(request, 'about.html')


def getMovieInformation( responseData ):

    data = {
        'id' :  responseData['id'],
        'title' : responseData['title'],
        'votes' : responseData['vote_count'],
        'rating' : responseData['vote_average'],
        'overview' : responseData['overview'],
        'genres' : [x['name'] for x in responseData['genres']],
        'homepage' : responseData['homepage'],
        'poster_path' : "https://image.tmdb.org/t/p/w500/" + responseData['poster_path'],
    }

    return data


def showMovieRecommendations(request, movie_id):

    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=73b7b94a31ab039b04bad943834342bd")
    responseData = response.json()

    # get details of the movie having id as movie_id.
    movieData = getMovieInformation(responseData)

    # getting recommending movie Data
    try:
        rec_movies = MovieRecommender.objects.get(movieId = movie_id)
        rec_movies_id = [rec_movies.movie1, rec_movies.movie2, rec_movies.movie3, rec_movies.movie4, rec_movies.movie5]
        rec_movies_data = []

        for id in rec_movies_id :
            response = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key=73b7b94a31ab039b04bad943834342bd")
            responseData = response.json()

            rec_movies_data.append( getMovieRecommendData(responseData) )
            

        return render(request, 'recommender.html', {'movieData' : movieData, 'rec_movies' : rec_movies_data})
    except:
        return render(request, 'recommender.html', {'movieData' : movieData})


from .forms import UserSignUpForm

# user signup
def signup(request):
    fm = UserSignUpForm()
    return render(request, 'signup.html', {'fm' : fm}) 


# user recommendations (for dashboard Page)
def userDashboard(request):
    
    if not request.user.is_authenticated :
        return HttpResponseRedirect('login')
    
    user = User.objects.get(username=request.user)
    user_id = int(user.username)

    #finding user id inside matrix movie recommender
    userObj = MatrixMovieRecommender.objects.get(userId = user_id)
    movie_ids = [userObj.movie1, userObj.movie2, userObj.movie3, userObj.movie4, userObj.movie5]

    # generating recommended movie data of the user..
    rec_movies = []
    for id in movie_ids :
        response = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key=73b7b94a31ab039b04bad943834342bd")
        responseData = response.json()

        if 'success' in responseData.keys():
            continue
        
        data = getMovieRecommendData(responseData)
        rec_movies.append(data)

    return render(request, 'dashboard.html', {'user_id' : user_id, 'rec_movies' : rec_movies})


## user model creation

# def generateUserModel(request):

#     User.objects.all().delete();

#     for i in range(0, 610):
#         if i == 576 :
#             continue
#         fm = User(username=str(i), password="shiva")
#         fm.save()
    
#     return HttpResponse("Users are created")



#user login

from .forms import UserLoginForm
from django.contrib.auth import login, logout

def userLogin(request):
    if not request.user.is_authenticated :

        if request.method == 'POST':

            u_name = request.POST['username']
            u_pass = request.POST['password']

            try:
                user = User.objects.get(username=u_name)
            except:
                fm = UserLoginForm()
                messages.error(request, 'Invalid credentials. Please Try Again !!')
                return render(request, 'login.html', {'fm' : fm})

            if user is not None :
                if u_pass != 'userpass':
                    fm = UserLoginForm()
                    messages.error(request, 'Invalid credentials. Please Try Again !!')
                    return render(request, 'login.html', {'fm' : fm})

                login(request, user)
                messages.success(request, 'User Logged In Successfully !!')

                return HttpResponseRedirect('/user/dashboard')
        else :
            fm = UserLoginForm()
            return render(request, 'login.html', {'fm' : fm})
    else :
        return HttpResponseRedirect('/user/dashboard')


#user logout
def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/')
    
# handle bad request
def badRequest(request):
    return HttpResponse("404!!! Page not found")