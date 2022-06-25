# import os
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







def getMoviesData( results ):

    data = []

    for x in results:
        movieData = {}
        movieData['id'] = x['id']
        movieData['title'] = x['title']
        movieData['votes'] = x['vote_count']
        movieData['rating'] = x['vote_average']
        movieData['poster_path'] = "https://image.tmdb.org/t/p/w500/" + x['poster_path']

        data.append(movieData)

    return data


# home page ... 
def homePage(request):
    response = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key=73b7b94a31ab039b04bad943834342bd&language=en-US&page=50")
    results = response.json()['results']
    
    data = getMoviesData(results)
        
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

def getMovieRecommendData( responseData ):
    
    data = {
        'id' :  responseData['id'],
        'title' : responseData['title'],
        'votes' : responseData['vote_count'],
        'rating' : responseData['vote_average'],
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


def generateMovieData( responseData ) :

    data = {
        'id' :  responseData['id'],
        'title' : responseData['title'],
        'votes' : responseData['vote_count'],
        'rating' : responseData['vote_average'],
        'poster_path' : "https://image.tmdb.org/t/p/w500/" + responseData['poster_path'],
    }

    return data;

# user recommendations (for dashboard Page)
def userDashboard(request):
    
    if not request.user.is_authenticated :
        return HttpResponseRedirect('login')
    
    user = User.objects.get(username=request.user)
    user_id = int(user.username)

    rec_choice = "1"

    if request.method == "POST" :
        rec_choice = request.POST['rec_choice']

        if rec_choice == "2" :
            userObj = MatrixMovieRecommender.objects.get(userId = user_id)
            movie_ids = [userObj.movie1, userObj.movie2, userObj.movie3, userObj.movie4, userObj.movie5]

            rec_movies = []
            for id in movie_ids :
                response = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key=73b7b94a31ab039b04bad943834342bd")
                responseData = response.json()

                if 'success' in responseData.keys():
                    continue
                    
                data = generateMovieData(responseData)
                rec_movies.append(data)

            return render(request, 'dashboard.html', {'user_id' : user_id, 'rec_movies' : rec_movies, 'second' : rec_choice})
    

    # finding user object inside collabarativeMovieRecommender 
    userObj = CollabarativeMovieRecommender.objects.get(userId = user_id)
    movie_ids = [userObj.movie1, userObj.movie2, userObj.movie3, userObj.movie4, userObj.movie5, userObj.movie6]


    # generating recommended movie data of the user..
    rec_movies = []
    for id in movie_ids :
        response = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key=73b7b94a31ab039b04bad943834342bd")
        responseData = response.json()

        if 'success' in responseData.keys():
            continue
        
        data = generateMovieData(responseData)
        rec_movies.append(data)

    return render(request, 'dashboard.html', {'user_id' : user_id, 'rec_movies' : rec_movies, 'first' : rec_choice})


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