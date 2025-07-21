from django.urls import path
from events.views import create_event, delete_event, edit_event, organizer_dashboard,view_events

urlpatterns = [
   path('create-event/',create_event, name='create_event'),
   path('dashboard/',organizer_dashboard,name='organizer_dashboard'),
   path('view-events/', view_events, name='view_events'),
   path('edit-event/<int:id>/',edit_event, name='edit_event'),
   path('delete-event/<int:id>',delete_event, name='delete_event'),
]