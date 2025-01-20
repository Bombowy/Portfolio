from django.db import models
from django.contrib.auth.models import User


# Enum for task statuses

class TaskStatus(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True)  # Używamy code jako klucz główny
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(
        TaskStatus,
        on_delete=models.PROTECT,
        related_name='tasks',
        default=0  # Domyślna wartość, odnosi się teraz do pola `code`
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Comment(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments'
    )


    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    content = models.TextField()


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"Comment by {self.author} on {self.task}"
