import django_filters
from django.db.models import Q
from .models import Queue

class QueueFilter(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(choices=Queue.STATUS_CHOICES)
    room_displayname = django_filters.CharFilter(field_name='room__displayname', lookup_expr='icontains')
    search = django_filters.CharFilter(method='filter_by_name_or_cccd')

    class Meta:
        model = Queue
        fields = ['status', 'room__displayname']
        
    def filter_by_name_or_cccd(self, queryset, name, value):
        return queryset.filter(Q(patient__full_name__icontains=value) | Q(patient__cccd__icontains=value))
