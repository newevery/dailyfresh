from django.contrib import admin
from django.urls import path,re_path
from . import views
from apps.user.views import RegisterView, ActiveView, LoginView

urlpatterns = [
    # path('register/', views.register, name='register'),
    # path('register_handle/',views.register_handle,name='register_handle'),

    path('register/', RegisterView.as_view(), name='register'),
    re_path('active/(?P<token>.*)',ActiveView.as_view(),name='active'),
    path('login/',LoginView.as_view(),name='login')
]