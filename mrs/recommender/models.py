from django.db import models

# Create your models here.

#bag of words (content based mrs) model
class MovieRecommender(models.Model):
    movieId = models.IntegerField(primary_key=True)
    movie1 = models.IntegerField()
    movie2 = models.IntegerField()
    movie3 = models.IntegerField()
    movie4 = models.IntegerField()
    movie5 = models.IntegerField()


#collaborative based model.
class CollabarativeMovieRecommender(models.Model):
    userId = models.IntegerField(primary_key=True)
    movie1 = models.IntegerField()
    movie2 = models.IntegerField()
    movie3 = models.IntegerField()
    movie4 = models.IntegerField()
    movie5 = models.IntegerField()
    movie6 = models.IntegerField()


#matrix factorization based model..
class MatrixMovieRecommender(models.Model):
    userId = models.IntegerField(primary_key=True)
    movie1 = models.IntegerField()
    movie2 = models.IntegerField()
    movie3 = models.IntegerField()
    movie4 = models.IntegerField()
    movie5 = models.IntegerField()