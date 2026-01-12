from django.urls import path
from .views import (
    bible, get_chapter_passage, 
    home, register, login_user, logout_user,
    forgot_password, reset_password
)

urlpatterns = [
    path('', home, name='home'),

    # auth
    path('register/', register, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:reset_id>/', reset_password, name='reset_user_password'),

    path('bible/', bible, name='bible'),
    path("api/bible/passage/", get_chapter_passage, name="get_chapter_passage"),
]