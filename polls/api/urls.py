from django.urls import path

from . import views

urlpatterns = [
    path('', views.PollActiveListAPIView.as_view()),
    path('create/', views.PollCreateAPIView.as_view()),
    path('<int:pk>/', views.PollDetailAPIView.as_view()),

    path('questions/', views.QuestionListAPIView.as_view()),
    path('questions/create/', views.QuestionCreateAPIView.as_view()),
    path('questions/<int:pk>/', views.QuestionDetailAPIView.as_view()),
    path('questions/<int:pk>/answer/', views.AnswerCreateAPIView.as_view()),

    path(
        'users/<int:user_id>/answers/',
        views.UserAnswerListAPIView.as_view()
    ),
]
