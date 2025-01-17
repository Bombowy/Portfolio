from django.contrib import admin
from .models import Task, Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'status', 'created_at')
    list_filter = ('status', 'due_date', 'assigned_to')
    search_fields = ('title', 'description')
    ordering = ('due_date',)
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('assigned_to',)
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('title', 'description', 'status', 'due_date', 'assigned_to')
        }),
        ('Czas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'content', 'created_at')
    search_fields = ('task__title', 'author__username', 'content')
    list_filter = ('created_at',)
    list_display_links = ('task',)
    readonly_fields = ('created_at',)
