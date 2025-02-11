from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from .permissions import user_has_permission
import json

from .models import Task, Project, ProjectMembership, Permission, Friendship, Comment, RolePermission
from .forms import UserRegisterForm, TaskForm , ProjectForm , ProjectRole
from django.db.models import Q
from .forms import CommentForm, ProjectRoleForm

def index(request):

    return render(request, 'index.html')


@login_required
def task_list(request):

    user_projects = Project.objects.filter(memberships__user=request.user).prefetch_related('roles__permissions')
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
            project_permissions[project.id] = set(
                membership.role.role_permissions.values_list("permission__name", flat=True)
            )

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

    if not user_membership:
        messages.error(request, "You do not have permission to view this project.")
        return redirect("task_list")

    project_members = User.objects.filter(project_memberships__role__project=project).distinct()
    project_roles = ProjectRole.objects.filter(project=project)
    global_roles = ProjectRole.objects.filter(project=None)
    can_add_role = False
    if user_membership:
        project_permissions = set(
            user_membership.role.role_permissions.values_list("permission__name", flat=True)
        )


        can_add_role = "ADD_ROLE" in project_permissions

    if request.method == "POST":
        form = ProjectRoleForm(request.POST)
        if form.is_valid():
            new_role = form.save(commit=False)
            new_role.project = project
            new_role.save()
            messages.success(request, f"Role '{new_role.name}' has been added to the project.")
            return redirect("project_task_list", project_id=project.id)
    else:
        form = ProjectRoleForm()

    project_permissions = {}
    if user_membership:
        project_permissions[project.id] = set(
            user_membership.role.permissions.values_list("name", flat=True)
        )



    return render(request, 'project_task_list.html', {
        'project': project,
        'tasks': tasks,
        'user_membership': user_membership,
        'project_permissions': project_permissions,
        'project_members': project_members,
        "project_roles": project_roles,
        "global_roles": global_roles,
        "form": form,
        "can_add_role": can_add_role
    })


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = task.comments.all()
    project = task.project

    if project is None and task.assigned_to != request.user:
        messages.error(request, "You do not have permission to view this task.")
        return redirect("task_list")

    if project and not ProjectMembership.objects.filter(project=project, user=request.user).exists():
        messages.error(request, "You do not have permission to view tasks in this project.")
        return redirect("task_list")

    can_add_comment = False
    if project is None:
        can_add_comment = task.assigned_to == request.user
    else:
        user_membership = ProjectMembership.objects.filter(project=project, user=request.user).first()
        if user_membership:
            project_permissions = set(user_membership.role.permissions.values_list("name", flat=True))

            can_add_comment = "CREATE_COMMENT" in project_permissions

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = CommentForm()

    return render(request,
        'task_detail.html',
            {'task': task,
             'comments': comments,
             'form': form,
             'project': task.project if hasattr(task, 'project') else None,
             'can_add_comment': can_add_comment
             })


@login_required
def create_task(request, project_id):

    project = None if project_id == 0 else get_object_or_404(Project, id=project_id)

    global_members = User.objects.filter(
        project_memberships__role__project__isnull=True
    ).distinct()

    project_members = User.objects.filter(
        project_memberships__role__project=project
    ).distinct() if project else User.objects.none()

    available_users = project_members.union(global_members)

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
        "project_members": available_users
    })


@login_required
def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)
    project = task.project


    project_members = User.objects.filter(
        id__in=ProjectMembership.objects.filter(project=project).values_list("user_id", flat=True)
    ) if project else None

    if project is None and task.assigned_to != request.user:
        messages.error(request, "You do not have permission to edit this task.")
        return redirect("task_list")

    can_edit = project is None or user_has_permission(request.user, project, "EDIT_TASK")
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
    if not user_membership or user_membership.role.name not in ['Owner']:
        return HttpResponseForbidden("You do not have permission to invite users to this project.")

    if request.method == 'POST':
        username = request.POST.get('username')
        role_id = request.POST.get('role')

        invited_user = get_object_or_404(User, username=username)
        role = get_object_or_404(ProjectRole, id=role_id)

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


            owner_role = ProjectRole.objects.get(name="Owner", project=None)


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
    friends_not_in_project = friends.exclude(id__in=project.members.values_list("id", flat=True))
    if request.method == "POST":
        username = request.POST.get("username")
        role_id = request.POST.get("role")

        user = get_object_or_404(User, username=username)
        role = get_object_or_404(ProjectRole, Q(id=role_id, project=project) | Q(id=role_id, project__isnull=True))  # 🔥 Ważne: obsługuje role globalne!

        if user not in friends:
            return HttpResponseForbidden("You can only add friends to the project.")

        ProjectMembership.objects.create(user=user, project=project, role=role)
        messages.success(request, f"{username} has been added to the project with role {role.name}.")
        return redirect("project_task_list", project_id=project.id)

    project_roles = ProjectRole.objects.filter(project=project)
    global_roles = ProjectRole.objects.filter(project__isnull=True)
    roles = project_roles | global_roles

    return render(request, "add_member.html", {"project": project, "roles": roles, "friends": friends_not_in_project})


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


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author:
        return HttpResponseForbidden("Nie masz uprawnień do edycji tego komentarza.")

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=comment.task.id)  # Wracamy na tę samą stronę po edycji

    return redirect('task_detail', task_id=comment.task.id)  # Jeśli coś poszło nie tak


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author:
        return HttpResponseForbidden("Nie masz uprawnień do usunięcia tego komentarza.")

    task_id = comment.task.id
    comment.delete()
    return redirect('task_detail', task_id=task_id)


@login_required
def project_roles_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user_membership = ProjectMembership.objects.filter(project=project, user=request.user).first()

    if not user_membership:
        messages.error(request, "You do not have permission to view roles in this project.")
        return redirect("task_list")

    can_add_role = "ADD_ROLE" in user_membership.role.permissions.values_list("name", flat=True)

    if not project.members.filter(id=request.user.id).exists():
        messages.error(request, "You do not have permission to view this project roles.")
        return redirect("task_list")

    project_roles = ProjectRole.objects.filter(project=project)
    default_roles = ProjectRole.objects.filter(project=None)
    all_permissions = Permission.objects.all()

    if request.method == "POST":
        role_id = request.POST.get("role_id")  # Pobieramy ID roli z formularza
        form = ProjectRoleForm(request.POST)

        if form.is_valid():
            if role_id:  # Jeśli istnieje ID roli, edytujemy ją zamiast tworzyć nową
                role = get_object_or_404(ProjectRole, id=role_id, project=project)
                role.name = form.cleaned_data["name"]
                role.save()

                # Usuwamy stare uprawnienia i dodajemy nowe
                RolePermission.objects.filter(role=role).delete()
                selected_permissions = form.cleaned_data["permissions"]
                RolePermission.objects.bulk_create(
                    [RolePermission(role=role, permission=perm) for perm in selected_permissions]
                )

                messages.success(request, f"Role '{role.name}' has been updated.")
            else:
                new_role = form.save(commit=False)
                new_role.project = project
                new_role.save()

                selected_permissions = form.cleaned_data["permissions"]
                RolePermission.objects.bulk_create(
                    [RolePermission(role=new_role, permission=perm) for perm in selected_permissions]
                )

                messages.success(request, f"Role '{new_role.name}' has been added to the project.")

            return redirect("project_roles_list", project_id=project.id)
    else:
        form = ProjectRoleForm()

    return render(request, "project_roles_list.html", {
        "project": project,
        "project_roles": project_roles,
        "default_roles": default_roles,
        "all_permissions": all_permissions,
        "can_add_role": can_add_role,
        "form": form
    })



@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)


    if not user_has_permission(request.user, project, "DELETE_PROJECT"):
        return HttpResponseForbidden("You do not have permission to delete this project.")

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully.")
        return redirect("task_list")


@login_required
def edit_role(request, project_id, role_id):
    project = get_object_or_404(Project, id=project_id)
    role = get_object_or_404(ProjectRole, id=role_id, project=project)


    if not user_has_permission(request.user, project, "ADD_ROLE"):
        return HttpResponseForbidden("You do not have permission to edit roles in this project.")

    if request.method == "POST":
        form = ProjectRoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, f"Role '{role.name}' has been updated successfully.")
            return redirect("project_roles_list", project_id=project.id)
    else:
        form = ProjectRoleForm(instance=role)

    return redirect("project_roles_list", project_id=project.id)


@login_required
def delete_role(request, project_id, role_id):
    project = get_object_or_404(Project, id=project_id)
    role = get_object_or_404(ProjectRole, id=role_id, project=project)


    if not user_has_permission(request.user, project, "ADD_ROLE"):
        return HttpResponseForbidden("You do not have permission to delete roles in this project.")


    if role.memberships.exists():
        messages.error(request, f"Cannot delete role '{role.name}' because it is assigned to users.")
        return redirect("project_roles_list", project_id=project.id)

    role.delete()
    messages.success(request, f"Role '{role.name}' has been deleted successfully.")
    return redirect("project_roles_list", project_id=project.id)




@login_required
def change_member_role(request, project_id, user_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        user_to_update = get_object_or_404(User, id=user_id)

        if not user_has_permission(request.user, project, "ADD_MEMBER"):
            return JsonResponse({"success": False, "error": "No permission"}, status=403)

        membership = ProjectMembership.objects.filter(user=user_to_update, project=project).first()
        if not membership:
            return JsonResponse({"success": False, "error": "User not in project"}, status=400)

        data = json.loads(request.body)
        new_role_id = data.get("new_role")
        new_role = get_object_or_404(ProjectRole, id=new_role_id)


        if new_role.project and new_role.project != project:
            return JsonResponse({"success": False, "error": "Invalid role for this project"}, status=400)

        membership.role = new_role
        membership.save()

        return JsonResponse({"success": True, "new_role": new_role.name})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

