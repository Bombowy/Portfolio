from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),


    path('list/', views.task_list, name='task_list'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/create/<int:project_id>/', views.create_task, name='create_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/assign/', views.assign_task, name='assign_task'),


    path('project/new/', views.create_project, name='create_project'),
    path('project/<int:project_id>/tasks/', views.project_task_list, name="project_task_list"),
    path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path("project/<int:project_id>/delete/", views.delete_project, name="delete_project"),


    path('project/<int:project_id>/add_member/', views.add_member, name='add_member'),
    path('project/<int:project_id>/remove_member/<int:user_id>/', views.remove_member, name='remove_member'),
    path('project/<int:project_id>/change_member_role/<int:user_id>/', views.change_member_role, name="change_member_role"),


    path("friends/add/", views.add_friend, name="add_friend"),
    path("friends/accept/<int:user_id>/", views.accept_friend, name="accept_friend"),
    path("friends/remove/<int:user_id>/", views.remove_friend, name="remove_friend"),
    path("friends/check_username/", views.check_username, name="check_username"),

    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    path("project/<int:project_id>/roles/", views.project_roles_list, name="project_roles_list"),
    path('project/<int:project_id>/role/<int:role_id>/edit/', views.edit_role, name="edit_role"),
    path('project/<int:project_id>/role/<int:role_id>/delete/', views.delete_role, name="delete_role"),

    path('register/', views.register, name='register'),
]
