from django.urls import path
from . import views

urlpatterns = [
    path(r'login', views.login, name='login'),
    path(r'login/', views.login), 
    path(r'signup/', views.signup, name='signup'),
    path(r'signup/', views.signup),
    path('detail/<int:event_id>/', views.detail, name='detail') #event_detail
]