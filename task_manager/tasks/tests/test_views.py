from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTest(TestCase):
    def test_registration_form_valid_data(self):
        """Tests user registration with valid data"""
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        })
        self.assertEqual(response.status_code, 302)  # Check if the response status is a redirect (302)
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Verify the user is created
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())  # Verify the email is saved

    def test_registration_form_invalid_data(self):
        """Tests user registration with invalid data"""
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123',
            'password2': 'DifferentPassword123',
        })
        self.assertEqual(response.status_code, 200)  # Form should be returned
        self.assertFalse(User.objects.filter(username='testuser').exists())  # User should not be created

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
        self.assertTrue(logged_in, "User was not logged in")  # Sprawdzenie poprawności logowania

        response = self.client.get(reverse('login'))
        print(f"Status Code: {response.status_code}")  # Debugowanie kodu odpowiedzi
        print(f"Redirect URL: {response.url}")  # Debugowanie przekierowania
        self.assertEqual(response.status_code, 302)  # Sprawdza, czy nastąpiło przekierowanie
        self.assertRedirects(response, '/tasks/')  # Sprawdza, czy przekierowano na /tasks/



from tasks.models import Task
from tasks.forms import TaskForm


class TaskViewsTest(TestCase):
    def setUp(self):
        """Set up initial data for tests"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(title="Test Task", description="Test Description")

    def test_index_view(self):
        """Test the index view"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_task_list_view_authenticated(self):
        """Test the task_list view for an authenticated user"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_list.html')
        self.assertContains(response, self.task.title)

    def test_task_list_view_unauthenticated(self):
        """Test the task_list view for an unauthenticated user"""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)  # Expected redirect to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('task_list')}")

    def test_task_detail_view_authenticated(self):
        """Test the task_detail view for an authenticated user"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_detail.html')
        self.assertContains(response, self.task.title)

    def test_task_detail_view_unauthenticated(self):
        """Test the task_detail view for an unauthenticated user"""
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Expected redirect to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('task_detail', args=[self.task.id])}")

    def test_create_task_view_authenticated(self):
        """Test the create_task view for an authenticated user"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_task'), {
            'title': 'New Task',
            'description': 'New Description'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to task_list
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_create_task_view_unauthenticated(self):
        """Test the create_task view for an unauthenticated user"""
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create_task')}")

    def test_edit_task_view_authenticated(self):
        """Test the edit_task view for an authenticated user"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to task_list
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_edit_task_view_unauthenticated(self):
        """Test the edit_task view for an unauthenticated user"""
        response = self.client.get(reverse('edit_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('edit_task', args=[self.task.id])}")

    def test_delete_task_view_authenticated(self):
        """Test the delete_task view for an authenticated user"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to task_list
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_view_unauthenticated(self):
        """Test the delete_task view for an unauthenticated user"""
        response = self.client.get(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('delete_task', args=[self.task.id])}")
