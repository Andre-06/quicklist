from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_request, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('verify/<str:verification_code>/', views.verify_email, name='verify_email'),
]
