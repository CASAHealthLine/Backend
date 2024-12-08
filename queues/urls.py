from django.urls import path
from .views import AddToQueueView, GetQueueView, GetSpecificQueueView, UpdateQueueStatusView

urlpatterns = [
    path('add-to-queue/', AddToQueueView.as_view(), name='add_to_queue'),
    path('queue/<int:queue_id>/update-status/', UpdateQueueStatusView.as_view(), name='update_queue_status'),
    path('queue/<int:room_id>/', GetSpecificQueueView.as_view(), name='get_queue'),
    path('queue/', GetQueueView.as_view(), name='get_all_queues'),
]