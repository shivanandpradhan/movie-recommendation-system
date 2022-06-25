from django.contrib import admin
from recommender.models import MovieRecommender, MatrixMovieRecommender, CollabarativeMovieRecommender

# Register your models here.

# registering content based movie recommender model to admin site.
@admin.register(MovieRecommender)
class MovieRecommenderAdmin(admin.ModelAdmin):
    list_display = ('movieId', 'movie1', 'movie2', 'movie3', 'movie4', 'movie5')


# registering collabarative movie recommender model to admin site.
@admin.register(CollabarativeMovieRecommender)
class CollabarativeMovieRecommenderAdmin(admin.ModelAdmin):
    list_display = ('userId', 'movie1', 'movie2', 'movie3', 'movie4', 'movie5', 'movie6')


# registering matrix factorization based movie recommender model to admin site.
@admin.register(MatrixMovieRecommender)
class CollabarativeMovieRecommenderAdmin(admin.ModelAdmin):
    list_display = ('userId', 'movie1', 'movie2', 'movie3', 'movie4', 'movie5')