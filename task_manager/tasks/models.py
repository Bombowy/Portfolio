from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TaskStatus(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tasks_task_status'

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    members = models.ManyToManyField(User, through='ProjectMembership', related_name='projects')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        default=0
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
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


class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'tasks_permission'

    def __str__(self):
        return self.name



class ProjectRole(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="roles", null=True, blank=True,)
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField("Permission", through="RolePermission", related_name="project_roles")

    class Meta:
        unique_together = ("project", "name")
        db_table = 'tasks_project_role'
    def __str__(self):
        return f"{self.name} ({self.project.name})"

class RolePermission(models.Model):
    role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey("Permission", on_delete=models.CASCADE, related_name="role_permissions")

    class Meta:
        unique_together = ('role', 'permission')
        db_table = 'tasks_role_permission'

    def __str__(self):
        return f"{self.role.name} - {self.permission.name} ({self.role.project.name})"


class ProjectMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_memberships")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    role = models.ForeignKey(ProjectRole, on_delete=models.PROTECT, related_name="memberships")

    class Meta:
        unique_together = ("user", "project")
        db_table = "tasks_project_membership"

    def __str__(self):
        return f"{self.user.username} - {self.role.name} in {self.project.name}"




class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends_initiated")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends_received")
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        status = "Accepted" if self.accepted else "Pending"
        return f"{self.user.username} → {self.friend.username} ({status})"

    def clean(self):
        """Ensure that a user cannot add themselves as a friend."""
        if self.user == self.friend:
            raise ValidationError("You cannot add yourself as a friend.")

    def save(self, *args, **kwargs):
        """Call clean() before saving to enforce validation."""
        self.clean()
        super().save(*args, **kwargs)



