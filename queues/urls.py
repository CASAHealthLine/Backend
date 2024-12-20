from django.urls import path
from .views import AddToQueueView, GetQueueView, GetSpecificQueueView, UpdateQueueStatusView, GetFilterFields, GetMyQueueView, GetMyCurrentQueueView

urlpatterns = [
    path('add/', AddToQueueView.as_view(), name='add_to_queue'),
    path('<int:queue_id>/update-status/', UpdateQueueStatusView.as_view(), name='update_queue_status'),
    path('<int:room_id>/', GetSpecificQueueView.as_view(), name='get_queue'),
    path('', GetQueueView.as_view(), name='get_all_queues'),
    path('filter/', GetFilterFields.as_view(), name='get_filter_fields'),
    path('my/', GetMyQueueView.as_view(), name='get_my_queue'),
    path('my/current/', GetMyCurrentQueueView.as_view(), name='get_current_queue'),
]