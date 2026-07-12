from django.urls import path
from . import views

urlpatterns = [
    # Task CRUD
    path('projects/<int:project_pk>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/status/', views.task_update_status, name='task_update_status'),

    # Comments
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),

    # Notifications
    path('notifications/', views.notifications, name='notifications'),
]
