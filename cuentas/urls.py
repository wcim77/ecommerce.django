from django.urls import path
from . import views


urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('panel/', views.panel, name='panel'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
   
]