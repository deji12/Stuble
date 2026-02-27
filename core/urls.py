from django.urls import path
from .views import (

    #admin
    send_out_bulk_email,

    # waiting list
    waiting_list,
    
    # bible
    bible, get_chapter_passage, 

    home, landing,
    
    # auth
    register, login_user, logout_user,
    forgot_password, reset_password, 
    delete_account, edit_account,
    
    # records
    create_record, user_records, 
    user_record, edit_record,
    delete_record,

    # collections
    user_collections, create_collection,
    edit_collection, delete_collection,
    user_collection
)

urlpatterns = [

    path('join-waitlist/', waiting_list, name='wait_list'),

    path('dashboard/', home, name='dashboard'),
    path('', landing, name='landing_page'),

    # auth
    path('register/', register, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:reset_id>/', reset_password, name='reset_user_password'),
    path('delete-account/', delete_account, name='delete_account'),
    path('settings/', edit_account, name='settings'),


    # bible
    path('bible/', bible, name='bible'),
    path("api/bible/passage/", get_chapter_passage, name="get_chapter_passage"),

    # records
    path('records/', user_records, name='user_records'),
    path('create-record/', create_record, name='create_record'),
    path('records/<int:record_id>/', user_record, name='user_record'),
    path('records/<int:record_id>/edit/', edit_record, name='edit_record'),
    path('records/<int:record_id>/delete/', delete_record, name='delete_record'),

    # collections
    path('collections/', user_collections, name='user_collections'),
    path('collections/<int:collection_id>/', user_collection, name='user_collection'),
    path('collections/create', create_collection, name='create_collection'),
    path('collections/edit', edit_collection, name='edit_collection'),
    path('collections/delete/', delete_collection, name='delete_collection'),

    # admin
    path('send-bulk-emails/', send_out_bulk_email, name='send_bulk_email'),
]