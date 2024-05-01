from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.QuizList.as_view()),
    path('quiz-create/', views.QuizCreate.as_view()),
    path('quiz-detail/<str:code>/', views.quiz_detail),
    path('answer-create/<str:code>/', views.answer_create),
    path('log-in/', views.log_in),
    path('log-out/', views.log_out),
    path('auth/', include('rest_framework.urls'))

]