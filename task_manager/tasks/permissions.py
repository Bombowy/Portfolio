from .models import ProjectMembership, Permission

DEFAULT_PERMISSIONS = [
    "CREATE_TASK",
    "ASSIGN_TASK",
    "DELETE_TASK",
    "ADD_MEMBER",
    "REMOVE_MEMBER",
    "EDIT_PROJECT",
    "EDIT_TASKS",
    "CREATE_COMMENT",
    "ADD_ROLE"
]


def initialize_permissions():

    for perm in DEFAULT_PERMISSIONS:
        Permission.objects.get_or_create(name=perm)


def user_has_permission(user, project, permission_name):


    membership = ProjectMembership.objects.filter(user=user, project=project).select_related('role').first()

    if not membership:
        return False

    return membership.role.permissions.filter(name=permission_name).exists()


