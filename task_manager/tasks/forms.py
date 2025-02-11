from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, Comment, ProjectRole, Permission

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }

class ProjectRoleForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select permissions for this role."
    )

    class Meta:
        model = ProjectRole
        fields = ["name", "permissions"]

    def save(self, commit=True):
        project_role = super().save(commit=False)
        if commit:
            project_role.save()
            self.save_m2m()
        return project_role