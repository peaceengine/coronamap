
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.create, name='create'),    
    path('<int:statement_id>', views.detail, name='detail'),
    path('<int:statement_id>/upvote', views.upvote, name='upvote'),
    path('<int:statement_id>/upvote_home', views.upvote_home, name='upvote_home')
]
