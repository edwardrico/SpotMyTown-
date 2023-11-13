from django.urls import path, include
from . import views
from .views import register, register_verification, verify_email

urlpatterns = [

    path('register_verification/', register_verification, name='register_verification'),
    path('verify_email/<int:user_id>/<str:token>/', verify_email, name='verify_email'),
    path('register/', views.register, name='register'),

]
