from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz-create/', views.quiz_create, name='quiz_create'),
    path('quiz-edit/<str:code>/', views.quiz_edit, name='quiz_edit'),
    path('quiz-delete/<str:code>/', views.quiz_delete, name='quiz_delete'),
    path('quiz-detail/<str:code>/', views.quiz_detail, name='quiz_detail'),
    path('question_create/', views.question_create, name='question_create'),
    path('options_create/<str:code>', views.options_create, name='options_create'),
    path('question_edit/<str:code>', views.question_edit, name='question_edit'),
    path('question_detail/<str:code>', views.question_detail, name='question_detail'),
    path('question_delete/<str:code>', views.question_delete, name='question_delete'),
    # -------------answer----------------
    path('answer-list/<str:code>/', views.answer_list, name='answer_list'),
    path('answer-detail/<str:code>', views.answer_detail, name='answer_detail'),
    # ------------auth-----------------
    path('sig-up/', views.sign_up, name='sign_up'),
    path('sig-in/', views.sign_in, name='sign_in'),
    path('log-out/', views.log_out, name='log_out'),
    # path('profile/', views.profile, name='profile'),
    # path('profile-update/', views.profile_update, name='profile_update'),
    # path('profile-delete/', views.profile_delete, name='profile_delete'),
]
