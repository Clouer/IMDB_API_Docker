from django.urls import path

from . import views

urlpatterns = [
    path('movie/', views.MovieListView.as_view()),
    path('movie/<int:pk>/', views.MovieDetailView.as_view()),
    path('review/', views.ReviewCreateView.as_view()),
    path('review/<int:pk>/', views.ReviewsView.as_view())

]
