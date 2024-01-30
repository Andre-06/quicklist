from django.urls import path
from . import views

urlpatterns = [
    path('your_lists/', views.lists, name="your_lists"),
    path('update_task/', views.update_task, name="update_task"),
]
