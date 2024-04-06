from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='mkulimabora_home'),
    path('contact/', views.contact_us, name='contactus'),
    path('gallery/', views.gallery, name="gallery"),
    path('subscribe', views.subscribe, name='subscribe'),
    path('login/', views.login_view, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.custom_logout, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('add-picture/', views.add_picture_to_gallery, name='add_picture'),
]