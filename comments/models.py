from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task


class Comment(models.Model):
    """
    Comment model, related to User and Task
    """
    owner = models.ForeignKey(User,  on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.TextField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    # def __str__(self): 
    #     return str(self.comment) if self.comment else 'No comment'
    def __str__(self):
        return str(self.comment) 
        
