from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task, Project, ProjectMembership, ProjectRole, Permission, RolePermission

class UserRegistrationTest(TestCase):
    def test_registration_form_valid_data(self):
        """Tests user registration with valid data"""
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())

    def test_registration_form_invalid_data(self):
        """Tests user registration with invalid data"""
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123',
            'password2': 'DifferentPassword123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())

class UserLoginTest(TestCase):
    def setUp(self):
        """Set up a user for login tests"""
        self.username = "testuser"
        self.password = "StrongPassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_valid_credentials(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tasks/')

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'WrongPassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_login_nonexistent_user(self):
        """Test login with nonexistent user"""
        response = self.client.post(reverse('login'), {
            'username': 'nonexistent',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_login_redirect_authenticated_user(self):
        """Test if already logged-in user is redirected"""
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertTrue(logged_in, "User was not logged in")

        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tasks/')






class TaskViewsTest(TestCase):

    def setUp(self):
        """Set up test data before each test."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")


        self.project = Project.objects.create(name="Test Project", owner=self.user)
        self.role = ProjectRole.objects.create(name="Manager")

        create_task_perm = Permission.objects.get_or_create(name="CREATE_TASK")[0]
        edit_task_perm = Permission.objects.get_or_create(name="EDIT_TASK")[0]
        delete_task_perm = Permission.objects.get_or_create(name="DELETE_TASK")[0]
        assign_task_perm = Permission.objects.get_or_create(name="ASSIGN_TASK")[0]


        RolePermission.objects.create(role=self.role, permission=create_task_perm)
        RolePermission.objects.create(role=self.role, permission=edit_task_perm)
        RolePermission.objects.create(role=self.role, permission=delete_task_perm)
        RolePermission.objects.create(role=self.role, permission=assign_task_perm)
        ProjectMembership.objects.create(user=self.user, project=self.project, role=self.role)


        self.task = Task.objects.create(
            title="Test Task",
            description="Task for testing",
            project=self.project,
            assigned_to=self.user
        )

    def test_index_view(self):
        """Test the index view"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_task_list_view_authenticated(self):
        """Test accessing the task list as an authenticated user."""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_task_list_view_unauthenticated(self):
        """Test accessing the task list as an unauthenticated user."""
        self.client.logout()
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('task_list')}")

    def test_task_detail_view_authenticated(self):
        """Test the task_detail view for an authenticated user"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_detail.html')
        self.assertContains(response, self.task.title)

    def test_task_detail_view_unauthenticated(self):
        """Test czy niezalogowany użytkownik jest przekierowany na login"""
        self.client.logout()
        response = self.client.get(reverse('task_detail', args=[self.task.id]), follow=True)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('task_detail', args=[self.task.id])}")

    def test_create_task_view_authenticated(self):
        """Test creating a task for an authenticated user with permissions."""
        response = self.client.post(reverse('create_task', kwargs={'project_id': self.project.id}), {
            'title': 'New Task',
            'description': 'New Description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_create_task_view_authenticated_no_project(self):
        """Test creating a task without a project (project_id=0)."""
        response = self.client.post(reverse('create_task', kwargs={'project_id': 0}), {
            'title': 'General Task',
            'description': 'General Description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='General Task').exists())

    def test_create_task_view_unauthenticated(self):
        """Test the create_task view for an unauthenticated user."""
        self.client.logout()
        response = self.client.get(reverse('create_task', kwargs={'project_id': 0}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create_task', kwargs={'project_id': 0})}")

    def test_edit_task_view_authenticated(self):
        """Test editing a task as an authenticated user with permissions."""
        response = self.client.post(reverse('edit_task', kwargs={'task_id': self.task.id}), {
            'title': 'Updated Task',
            'description': 'Updated Description'
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_edit_task_view_unauthenticated(self):
        """Test trying to edit a task without being logged in."""
        self.client.logout()
        response = self.client.post(reverse('edit_task', kwargs={'task_id': self.task.id}), {
            'title': 'Updated Task',
            'description': 'Updated Description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f"{reverse('login')}?next={reverse('edit_task', kwargs={'task_id': self.task.id})}")

    def test_delete_task_view_authenticated(self):
        """Test deleting a task for an authenticated user with permissions."""
        response = self.client.post(reverse('delete_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_view_unauthenticated(self):
        """Test trying to delete a task without being logged in."""
        self.client.logout()
        response = self.client.post(reverse('delete_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f"{reverse('login')}?next={reverse('delete_task', kwargs={'task_id': self.task.id})}")
