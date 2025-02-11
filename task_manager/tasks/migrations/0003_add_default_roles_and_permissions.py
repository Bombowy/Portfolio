import django.db.models.deletion
from django.db import migrations, models

def create_default_roles_and_permissions(apps, schema_editor):
    ProjectRole = apps.get_model("tasks", "ProjectRole")
    Permission = apps.get_model("tasks", "Permission")
    RolePermission = apps.get_model("tasks", "RolePermission")
    Project = apps.get_model("tasks", "Project")


    permissions = [
        {"name": "CREATE_TASK", "description": "Can create tasks"},
        {"name": "ASSIGN_TASK", "description": "Can assign tasks"},
        {"name": "DELETE_TASK", "description": "Can delete tasks"},
        {"name": "ADD_MEMBER", "description": "Can add members to project"},
        {"name": "REMOVE_MEMBER", "description": "Can remove members from project"},
        {"name": "EDIT_PROJECT", "description": "Can edit project details"},
        {"name": "EDIT_TASK", "description": "Can edit tasks"},
        {"name": "CREATE_COMMENT", "description": "Can create comments"},
        {"name": "ADD_ROLE", "description": "Can create new roles in project"},
        {"name": "DELETE_PROJECT", "description": "Can delete project"},
    ]


    existing_permissions = set(Permission.objects.values_list("name", flat=True))
    new_permissions = [Permission(**perm) for perm in permissions if perm["name"] not in existing_permissions]

    if new_permissions:
        Permission.objects.bulk_create(new_permissions)



    permission_map = {p.name: p for p in Permission.objects.all()}


    projects = Project.objects.all()

    if projects.exists():
        for project in projects:
            owner_role, created_owner = ProjectRole.objects.get_or_create(project=project, name="Owner")
            member_role, created_member = ProjectRole.objects.get_or_create(project=project, name="Member")



            role_permissions = [
                (owner_role, permission_map["CREATE_TASK"]),
                (owner_role, permission_map["ASSIGN_TASK"]),
                (owner_role, permission_map["DELETE_TASK"]),
                (owner_role, permission_map["ADD_MEMBER"]),
                (owner_role, permission_map["REMOVE_MEMBER"]),
                (owner_role, permission_map["EDIT_PROJECT"]),
                (owner_role, permission_map["EDIT_TASK"]),
                (owner_role, permission_map["CREATE_COMMENT"]),
                (owner_role, permission_map["ADD_ROLE"]),
                (owner_role, permission_map["DELETE_PROJECT"]),
                (member_role, permission_map["CREATE_COMMENT"]),
            ]

            role_permission_objects = [RolePermission(role=role, permission=perm) for role, perm in role_permissions]
            RolePermission.objects.bulk_create(role_permission_objects, ignore_conflicts=True)
    else:

        owner_role, created_owner = ProjectRole.objects.get_or_create(name="Owner", defaults={"project": None})
        member_role, created_member = ProjectRole.objects.get_or_create(name="Member", defaults={"project": None})


        role_permissions = [
            (owner_role, permission_map["CREATE_TASK"]),
            (owner_role, permission_map["ASSIGN_TASK"]),
            (owner_role, permission_map["DELETE_TASK"]),
            (owner_role, permission_map["ADD_MEMBER"]),
            (owner_role, permission_map["REMOVE_MEMBER"]),
            (owner_role, permission_map["EDIT_PROJECT"]),
            (owner_role, permission_map["EDIT_TASK"]),
            (owner_role, permission_map["CREATE_COMMENT"]),
            (owner_role, permission_map["ADD_ROLE"]),
            (owner_role, permission_map["DELETE_PROJECT"]),
            (member_role, permission_map["CREATE_COMMENT"]),
        ]

        role_permission_objects = [RolePermission(role=role, permission=perm) for role, perm in role_permissions]
        RolePermission.objects.bulk_create(role_permission_objects, ignore_conflicts=True)



class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_permission_role_taskstatus_project_task_project_and_more"),
    ]

    operations = [
        migrations.RunPython(create_default_roles_and_permissions),
    ]
