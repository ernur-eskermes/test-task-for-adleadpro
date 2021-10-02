from django.urls import path

from . import views

urlpatterns = [
    path('', views.PollActiveListAPIView.as_view(), name='poll-list'),
    path('create/', views.PollCreateAPIView.as_view(), name='poll-create'),
    path('<int:pk>/', views.PollDetailAPIView.as_view(), name='poll-detail'),

    path(
        '<int:poll_id>/questions/',
        views.QuestionListAPIView.as_view(),
        name='q-list'
    ),
    path(
        '<int:poll_id>/questions/create/',
        views.QuestionCreateAPIView.as_view(),
        name='q-create'
    ),
    path(
        '<int:poll_id>/questions/<int:pk>/',
        views.QuestionDetailAPIView.as_view(),
        name='q-detail'
    ),

    path(
        '<int:poll_id>/questions/<int:pk>/answer/',
        views.AnswerCreateAPIView.as_view(),
        name='answer-create'
    ),
    path(
        'users/<int:user_id>/answers/',
        views.UserAnswerListAPIView.as_view(),
        name='user-answers'
    ),
]
