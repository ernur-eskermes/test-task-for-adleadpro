from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.PollActiveListAPIView.as_view()
    ),

    path(
        'users/<int:pk>/answers/',
        views.UserAnswerListAPIView.as_view()
    ),

    path(
        '<int:poll_id>/questions/<int:q_id>/answer/',
        views.AnswerCreateAPIView.as_view()
    ),
]
