from django.urls import path
from . import views

urlpatterns = [
    path('', views.bannerPage, name='banner'),
    path('home', views.homePage, name='home'),
    path('about',views.aboutPage, name='about'),
    path('movie/<int:movie_id>', views.showMovieRecommendations, name='recommend_movie'),
    path('user/signup', views.signup),
    path('user/login', views.userLogin, name='login'),
    path('user/dashboard', views.userDashboard, name='dashboard'),
    path('user/logout', views.userLogout, name='logout'),

]

