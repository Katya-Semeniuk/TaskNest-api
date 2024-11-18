from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.TaskList.as_view()),
    path('tasks/<int:pk>/', views.TaskDetail.as_view()),
    path('tasks/<int:pk>/assign/', views.AssignUserToTaskView.as_view(), name='assign-user'),
    path('tasks/<int:pk>/unassign/', views.UnassignUserFromTaskView.as_view(), name='unassign-user'),
]