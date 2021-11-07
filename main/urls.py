from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register.as_view(), name='register'),
    path('login/', views.my_login.as_view(), name='login'),
    path('logout/', views.my_logout.as_view(), name='logout'),
    path('index/', views.index.as_view()),
    path('info/', views.info.as_view()),
    path('edit_info/', views.edit_info.as_view()),
    path('submit_lesson/', views.submit_lesson.as_view()),
    path('add_lesson/', views.add_lesson.as_view()),
    path('choice_lesson/', views.choice_lesson.as_view()),
    path('del_lesson/', views.del_lesson.as_view()),
    #path(r'^$', views.my_login.as_view()),
]
