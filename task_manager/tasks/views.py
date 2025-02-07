from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from .permissions import user_has_permission

from .models import Task, Project, ProjectMembership, Role, Friendship
from .forms import UserRegisterForm, TaskForm , ProjectForm
from django.db.models import Q

def index(request):

    return render(request, 'index.html')


@login_required
def task_list(request):

    user_projects = Project.objects.filter(memberships__user=request.user).prefetch_related('memberships__role__permissions')
    tasks = Task.objects.filter(assigned_to=request.user)


    friends = User.objects.filter(
        Q(friends_received__user=request.user, friends_received__accepted=True) |
        Q(friends_initiated__friend=request.user, friends_initiated__accepted=True)
    ).distinct()


    friend_requests = Friendship.objects.filter(friend=request.user, accepted=False).select_related("user")


    project_permissions = {}
    for project in user_projects:
        membership = project.memberships.filter(user=request.user).first()
        if membership:
            project_permissions[project.id] = set(membership.role.permissions.values_list("permission__name", flat=True))

    return render(request, 'task_list.html', {
        'tasks': tasks,
        'projects': user_projects,
        'project_permissions': project_permissions,
        'friends': friends,
        'friend_requests': friend_requests
    })



@login_required
def project_task_list(request, project_id):

    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)

    user_membership = ProjectMembership.objects.filter(project=project, user=request.user).first()

    project_members = User.objects.filter(project_roles__project=project).distinct()


    project_permissions = {}
    if user_membership:
        project_permissions[project.id] = set(user_membership.role.permissions.values_list("permission__name", flat=True))
    print(f"DEBUG: project_permissions dla {request.user.username} = {project_permissions}")  # 👈 Debug tutaj

    return render(request, 'project_task_list.html', {
        'project': project,
        'tasks': tasks,
        'user_membership': user_membership,
        'project_permissions': project_permissions,
        'project_members': project_members
    })


@login_required
def task_detail(request, task_id):

    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {'task': task})


@login_required
def create_task(request, project_id):

    project = None if project_id == 0 else get_object_or_404(Project, id=project_id)


    project_members = User.objects.filter(project_roles__project=project).distinct() if project else []


    if project and not user_has_permission(request.user, project, "CREATE_TASK"):
        return HttpResponseForbidden("You do not have permission to create tasks in this project.")

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            assigned_user_id = request.POST.get("assigned_to")


            if assigned_user_id and project:
                task.assigned_to = get_object_or_404(User, id=assigned_user_id)


            if not project:
                task.assigned_to = request.user

            task.save()
            messages.success(request, "Task created successfully.")
            return redirect("project_task_list", project_id=project.id) if project else redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "create_task.html", {
        "form": form,
        "project": project,
        "project_members": project_members
    })


@login_required
def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)
    project = task.project


    project_members = User.objects.filter(
        id__in=ProjectMembership.objects.filter(project=project).values_list("user_id", flat=True)
    ) if project else None


    can_edit = project is None or user_has_permission(request.user, project, "EDIT_TASKS")
    can_assign = project and user_has_permission(request.user, project, "ASSIGN_TASK")

    if not can_edit:
        return HttpResponseForbidden("You do not have permission to edit this task.")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)


            if not project:
                task.assigned_to = request.user


            elif can_assign:

                assigned_user_id = request.POST.get("assigned_to")
                if assigned_user_id:
                    assigned_user = get_object_or_404(User, id=assigned_user_id)
                    task.assigned_to = assigned_user


            task.save()


            messages.success(request, "Task successfully updated.")
            return redirect('project_task_list', project_id=project.id) if project else redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {
        'form': form,
        'task': task,
        'project': project,
        'can_assign': can_assign,
        'project_members': project_members
    })


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project

    if project and not user_has_permission(request.user, project, "DELETE_TASK"):
        return HttpResponseForbidden("You do not have permission to delete tasks.")

    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully.")

        if project:
            return redirect("project_task_list", project_id=project.id)

    return redirect("task_list")



def register(request):

    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account for {username} has been created! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def invite_user(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    user_membership = ProjectMembership.objects.filter(project=project, user=request.user).first()
    if not user_membership or user_membership.role.name not in ['Owner', 'Co-Owner']:
        return HttpResponseForbidden("You do not have permission to invite users to this project.")

    if request.method == 'POST':
        username = request.POST.get('username')
        role_id = request.POST.get('role')

        invited_user = get_object_or_404(User, username=username)
        role = get_object_or_404(Role, id=role_id)

        ProjectMembership.objects.create(user=invited_user, project=project, role=role)
        messages.success(request, f"User {username} has been invited to the project.")

    return redirect('project_task_list', project_id=project.id)


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            owner_role, _ = Role.objects.get_or_create(name="Owner")
            ProjectMembership.objects.create(user=request.user, project=project, role=owner_role)

            messages.success(request, 'Project created successfully.')
            return redirect('task_list')
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})

@login_required
def assign_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)
    project = task.project

    if not user_has_permission(request.user, project, "ASSIGN_TASK"):
        return HttpResponseForbidden("You do not have permission to assign tasks.")

    if request.method == "POST":
        assigned_user_id = request.POST.get("assigned_to")
        assigned_user = get_object_or_404(User, id=assigned_user_id)
        task.assigned_to = assigned_user
        task.save()
        messages.success(request, "Task assigned successfully.")
        return redirect("project_task_list", project_id=project.id)

    return render(request, "assign_task.html", {"task": task, "project": project})

@login_required
def add_member(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not user_has_permission(request.user, project, "ADD_MEMBER"):
        return HttpResponseForbidden("You do not have permission to add members.")

    friends = User.objects.filter(
        Q(friends_received__user=request.user, friends_received__accepted=True) |
        Q(friends_initiated__friend=request.user, friends_initiated__accepted=True)
    ).distinct()

    if request.method == "POST":
        username = request.POST.get("username")
        role_id = request.POST.get("role")
        user = get_object_or_404(User, username=username)
        role = get_object_or_404(Role, id=role_id)

        if user not in friends:
            return HttpResponseForbidden("You can only add friends to the project.")

        ProjectMembership.objects.create(user=user, project=project, role=role)
        messages.success(request, f"{username} has been added to the project.")
        return redirect("project_task_list", project_id=project.id)

    roles = Role.objects.all()
    return render(request, "add_member.html", {"project": project, "roles": roles, "friends": friends})


@login_required
def remove_member(request, project_id, user_id):

    project = get_object_or_404(Project, id=project_id)
    user_to_remove = get_object_or_404(User, id=user_id)


    if not user_has_permission(request.user, project, "REMOVE_MEMBER"):
        return HttpResponseForbidden("You do not have permission to remove members.")


    if request.user == user_to_remove:
        messages.error(request, "You cannot remove yourself from the project.")
        return redirect("project_task_list", project_id=project.id)


    owner_membership = ProjectMembership.objects.filter(project=project, role__name="Owner").first()
    if owner_membership and owner_membership.user == user_to_remove:
        messages.error(request, "You cannot remove the owner of the project.")
        return redirect("project_task_list", project_id=project.id)

    membership = ProjectMembership.objects.filter(user=user_to_remove, project=project).first()
    if membership:
        membership.delete()
        messages.success(request, f"{user_to_remove.username} has been removed from the project.")
    else:
        messages.error(request, "This user is not a member of the project.")

    return redirect("project_task_list", project_id=project.id)


@login_required
def edit_project(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    if not user_has_permission(request.user, project, "EDIT_PROJECT"):
        return HttpResponseForbidden("You do not have permission to edit this project.")

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully.")
            return redirect("project_task_list", project_id=project.id)
    else:
        form = ProjectForm(instance=project)

    return render(request, "edit_project.html", {"form": form, "project": project})


@login_required
def add_friend(request):

    if request.method == "POST":
        friend_username = request.POST.get("friend_username")
        friend = get_object_or_404(User, username=friend_username)  #

        if Friendship.objects.filter(Q(user=request.user, friend=friend) | Q(user=friend, friend=request.user)).exists():
            messages.error(request, "You are already friends or request is pending.")
        else:
            Friendship.objects.create(user=request.user, friend=friend)
            messages.success(request, f"Friend request sent to {friend.username}.")

    return redirect("task_list")



@login_required
def accept_friend(request, user_id):

    friendship = get_object_or_404(Friendship, user_id=user_id, friend=request.user, accepted=False)
    friendship.accepted = True
    friendship.save()
    messages.success(request, f"You are now friends with {friendship.user.username}.")
    return redirect("task_list")



@login_required
def remove_friend(request, user_id):

    friendship = Friendship.objects.filter(
        (Q(user=request.user, friend_id=user_id) | Q(user_id=user_id, friend=request.user))
    ).first()

    if friendship:
        friendship.delete()
        messages.success(request, "Friendship removed.")
    return redirect("task_list")

@login_required
def check_username(request):

    username = request.GET.get("username", "").strip()
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})