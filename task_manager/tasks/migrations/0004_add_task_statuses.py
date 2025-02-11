from django.db import migrations

def create_task_statuses(apps, schema_editor):
    TaskStatus = apps.get_model("tasks", "TaskStatus")

    statuses = [
        (0, "To Do", "Task is not started yet"),
        (1, "In Progress", "Task is currently being worked on"),
        (2, "Done", "Task is completed"),
    ]

    for code, name, description in statuses:
        TaskStatus.objects.get_or_create(code=code, defaults={"name": name, "description": description})

class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0003_add_default_roles_and_permissions"),
    ]

    operations = [
        migrations.RunPython(create_task_statuses),
    ]
