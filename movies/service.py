from django_filters import rest_framework as filter
from .models import Movie


def get_client_ip(request):
    """Получение ip пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


class CharFilterInFilter(filter.BaseInFilter, filter.CharFilter):
    pass


class MovieFilter(filter.FilterSet):
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    year = filter.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year']
