from django.urls import path
from .views import bible, get_chapter_passage, home

urlpatterns = [
    path('', home, name='home'),
    path('bible/', bible, name='bible'),
    path("api/bible/passage/", get_chapter_passage, name="get_chapter_passage"),
]