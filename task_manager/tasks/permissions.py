
from .models import ProjectMembership


def user_has_permission(user, project, permission_name):

    membership = ProjectMembership.objects.filter(user=user, project=project).select_related('role').first()

    if not membership:
        return False

    return membership.role.permissions.filter(permission__name=permission_name).exists()
