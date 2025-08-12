from django.db import models
from apps.users_management.models import UserManagement

class TaskManager(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('terminated', 'Terminated'),
    ]

    # Primary key 'id' is added automatically by Django, no need to declare explicitly
    task_unique_id = models.CharField(max_length=100, unique=True)
    task_username = models.ForeignKey(UserManagement,to_field='username', on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    task_tat = models.DurationField(help_text="Turnaround time for the task")
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task_name} ({self.task_unique_id})"
    class Meta:
        db_table : "task_management"