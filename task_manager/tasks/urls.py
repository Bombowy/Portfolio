from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.task_list, name='task_list'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),

]
