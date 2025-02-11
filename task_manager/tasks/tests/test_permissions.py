import pytest
from django.contrib.auth.models import User
from tasks.models import Task, Comment, Project, ProjectMembership, ProjectRole
from datetime import date
from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
class TestPermissions:
    @pytest.fixture
    def setup_data(self):
        owner_role = ProjectRole.objects.create(name="Test1")
        member_role = ProjectRole.objects.create(name="Test2")

        owner = User.objects.create_user(username="owner", password="password")
        member = User.objects.create_user(username="member", password="password")


        project = Project.objects.create(name="Test Project", description="A test project", owner=owner)
        ProjectMembership.objects.create(user=owner, project=project, role=owner_role)
        ProjectMembership.objects.create(user=member, project=project, role=member_role)

        task = Task.objects.create(title="Test Task", description="Task for testing", due_date=date(2025, 1, 31),
                                   assigned_to=member)
        comment = Comment.objects.create(task=task, author=member, content="Test Comment")

        return owner, member, project, task, comment



    def test_user_can_edit_own_task(self, setup_data):
        """Test that assigned user can edit their task"""
        _, member, _, task, _ = setup_data
        client = Client()
        client.force_login(member)

        response = client.post(reverse("edit_task", args=[task.id]), {"title": "Updated Task Title"})

        assert response.status_code == 302
        task.refresh_from_db()
        assert task.title == "Updated Task Title"

    def test_user_cannot_edit_others_tasks(self, setup_data):
        """Test that user cannot edit task they are not assigned to"""
        owner, _, _, task, _ = setup_data
        client = Client()
        client.force_login(owner)

        response = client.post(reverse("edit_task", args=[task.id]), {"title": "Malicious Edit"})

        assert response.status_code == 302

    def test_user_can_delete_own_comment(self, setup_data):
        """Test that users can delete their own comments"""
        _, member, _, _, comment = setup_data
        client = Client()
        client.force_login(member)

        response = client.post(reverse("delete_comment", args=[comment.id]))

        assert response.status_code == 302
        assert not Comment.objects.filter(id=comment.id).exists()

    def test_user_cannot_delete_others_comment(self, setup_data):
        """Test that users cannot delete comments from others"""
        owner, _, _, _, comment = setup_data
        client = Client()
        client.force_login(owner)

        response = client.post(reverse("delete_comment", args=[comment.id]))

        assert response.status_code == 403
