from django.urls import path
from . import views

urlpatterns = [
    path("", views.create_event, name="create_event"),
    path("events/", views.events_list, name="events_list"),
    path("event/<uuid:uid>/", views.event_detail, name="event_detail"),
    path("event/<uuid:uid>/pause/", views.pause_event, name="pause_event"),
    path("event/<uuid:uid>/resume/", views.resume_event, name="resume_event"),
    path("event/<uuid:uid>/delete/", views.delete_event, name="delete_event"),
    path('events/', views.events_list, name='events_list'),
]
