from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task, Comment, TaskStatus
from datetime import date


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up initial data for Task model tests"""
        cls.status_todo = TaskStatus.objects.get(code=0)
        cls.status_in_progress = TaskStatus.objects.get(code = 1)
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

        cls.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            due_date=date(2025, 1, 31),
            status=cls.status_todo,
            assigned_to=cls.user
        )

    def test_task_creation(self):
        """Test creating a Task instance"""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "This is a test task")
        self.assertEqual(self.task.due_date, date(2025, 1, 31))
        self.assertEqual(self.task.status, self.status_todo)
        self.assertEqual(self.task.assigned_to, self.user)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)

    def test_task_status_choices(self):
        """Test the Task status choices"""
        self.assertEqual(self.task.status, self.status_todo)
        self.task.status = self.status_in_progress
        self.task.save()
        self.assertEqual(self.task.status, self.status_in_progress)

    def test_task_string_representation(self):
        """Test the string representation of the Task model"""
        self.assertEqual(str(self.task), "Test Task")

class CommentModelTest(TestCase):
    def setUp(self):
        """Set up initial data for the Comment model tests"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task"
        )
        self.comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content="This is a test comment"
        )

    def test_comment_creation(self):
        """Test creating a Comment instance"""
        self.assertEqual(self.comment.task, self.task)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.content, "This is a test comment")
        self.assertIsNotNone(self.comment.created_at)

    def test_comment_string_representation(self):
        """Test the string representation of the Comment model"""
        self.assertEqual(str(self.comment), f"Comment by {self.user} on {self.task}")

