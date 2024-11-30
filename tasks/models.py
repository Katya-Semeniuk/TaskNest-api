from django.db import models
from django.contrib.auth.models import User


PRIORITY_CHOICES = [
    ('high', 'high'),
    ('medium', 'medium'),
    ('low', 'low'),
    ]
CATEGORY_CHOICES = [
    ('work', 'work'),
    ('home', 'home'),
    ('others', 'others'),
    ]


STATUS_CHOICES = [
    ('not-started', 'not started'),
    ('in-progress', 'in-progress'),
    ('complete', 'completed'),
    ]



class Task(models.Model):

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks'
    ) 
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
        choices=STATUS_CHOICES,
        default='not-started'
        )
    assigned_to = models.ManyToManyField(User, blank=True,)



    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Task: #{self.title}"

    def mark_overdue(self):
        """Mark task as overdue if due_date is passed."""
        if self.due_date and self.due_date < timezone.now().date():
            self.is_overdue = True
            self.save()