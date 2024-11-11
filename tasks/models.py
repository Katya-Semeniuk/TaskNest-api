from django.db import models
from django.contrib.auth.models import User


PRIORITY_CHOICES = [
        ('HIGH', 'high'),
        ('MEDIUM', 'medium'),
        ('LOW', 'low'),
]
CATEGORY_CHOICES = [
        ('Work', 'work'),
        ('Home', 'home'),
        ('OTHERS', 'others'),
    ]


STATUS = [
        ('NOT-STARTED', 'not started'),
        ('IN-PROGRESS', 'in-progress'),
        ('COMPLETE', 'completed'),
]


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_overdue = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
        )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='work'
        )
    status = models.CharField(
        max_length=255,
        choices=STATUS,
        default='not started'
        )
    assigned_to = models.ForeignKey(User, blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='assigned_to')



    class Meta:
        ordering = ['-id']

    def __str__(self):
        f"Task: #{self.title}"

    def mark_overdue(self):
        """Mark task as overdue if due_date is passed."""
        if self.due_date and self.due_date < timezone.now().date():
            self.is_overdue = True
            self.save()