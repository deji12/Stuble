from django.urls import path
from .views import (

    # waiting list
    waiting_list,
    
    # bible
    bible, get_chapter_passage, 

    home, 
    
    # auth
    register, login_user, logout_user,
    forgot_password, reset_password, 
    
    # records
    create_record, user_records, 
    user_record, edit_record,
    delete_record
)

urlpatterns = [

    path('', waiting_list, name='waiting_list'),

    # path('', home, name='home'),

    # auth
    # path('register/', register, name='register_user'),
    # path('login/', login_user, name='login_user'),
    # path('logout/', logout_user, name='logout_user'),
    # path('forgot-password/', forgot_password, name='forgot_password'),
    # path('reset-password/<str:reset_id>/', reset_password, name='reset_user_password'),

    # # bible
    # path('bible/', bible, name='bible'),
    # path("api/bible/passage/", get_chapter_passage, name="get_chapter_passage"),

    # # records
    # path('create-record/', create_record, name='create_record'),
    # path('records/', user_records, name='user_records'),
    # path('records/<int:record_id>/', user_record, name='user_record'),
    # path('records/<int:record_id>/edit/', edit_record, name='edit_record'),
    # path('records/<int:record_id>/delete/', delete_record, name='delete_record'),
]