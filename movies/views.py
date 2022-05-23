from django.db import models
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    ReviewSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer
)
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=(models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings')))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.filter(draft=False)


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class ReviewsView(APIView):
    """Вывод отзыва"""

    def get(self, request, pk):
        reviews = Movie.objects.get(id=pk).reviews
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга к фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """Вывод информации об актере"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
