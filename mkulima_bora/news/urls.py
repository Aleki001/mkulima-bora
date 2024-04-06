from django.urls import path
from . import views

urlpatterns = [
    path('mkulima-news/', views.kilimo_news, name='news'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('create-post/', views.create_post, name='create_post'),
]