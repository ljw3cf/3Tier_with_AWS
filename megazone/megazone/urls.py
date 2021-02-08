from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'megazone'

urlpatterns = [
    path('main/', views.index, name='index'),
    path('board/', views.board, name='board'),
    path('board/<int:question_id>/', views.board_detail, name='board_detail'),
    path('answer/create/<int:question_id>/', views.reply_create, name='reply_create'),
    path('board/create/', views.board_create, name='board_create'),
    path('', auth_views.LoginView.as_view(template_name='megazone/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]

