from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.logar, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
]
