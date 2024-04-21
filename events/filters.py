import django_filters

from events.models import Event


class EventMyFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    is_expired = django_filters.BooleanFilter()

    class Meta:
        model = Event
        fields = ['title', 'is_expired']
