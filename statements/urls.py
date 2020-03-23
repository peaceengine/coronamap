
from django.urls import path, include
from . import views

#app_name = 'statements'
urlpatterns = [
    path('', views.home, name='home'),  #index
    path('create', views.create, name='create'),    
    path('<int:statement_id>', views.detail, name='detail'),
    path('<int:statement_id>/results', views.results, name='results'),
    path('<int:statement_id>/giveResponseDisagree', views.giveResponseDisagree, name='giveResponseDisagree'),
    path('<int:statement_id>/giveResponseAgree', views.giveResponseAgree, name='giveResponseAgree'),
#    path('<int:statement_id>/upvote', views.upvote, name='upvote'),
#    path('<int:statement_id>/upvote_home', views.upvote_home, name='upvote_home')
]
