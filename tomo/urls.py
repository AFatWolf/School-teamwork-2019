from django.urls import path
from . import views

urlpatterns = [
    path(r'login', views.login, name='login'),
    path(r'login/', views.login),
    path(r'logout', views.logout, name='logout'),
    path(r'addtags', views.addTags, name='addTags'), 
    path(r'signup', views.signup, name='signup'),
    path(r'signup/', views.signup),
    path(r'index/', views.index, name = 'index'),
    path(r'index', views.index, name = 'index'),
    path('detail/<int:event_id>/', views.detail, name='detail'), #event_detail
    path(r'detail/<int:event_id>/update', views.update, name = 'update'),
    path(r'create', views.create, name = 'create'),
    path(r'/profile/<str:user_name>/', views.profile, name='user_profile'),
    path(r'settings/', views.settings, name='settings'),
    #path(r'settings/change_password/', views.change_password, name='change_password'),
]