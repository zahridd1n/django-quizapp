from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz-create/', views.quiz_create, name='quiz_create'),
    path('quiz-detail/<str:code>/', views.quiz_detail, name='quiz_detail'),
    path('question_create/', views.question_create, name='question_create'),
    path('question_detail/<str:code>', views.question_detail, name='question_detail'),
]
