from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user



class IsAssignedOrOwner(permissions.BasePermission):
    """
    Allows everyone to view comments, but only the assigned user
    or owner of the task can create or modify a comment.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if view.action == 'create':
            task_id = request.data.get('task')
            if not task_id:
                return False
            
            try:
                from tasks.models import Task 
                task = Task.objects.get(pk=task_id)
                return task.owner == request.user or task.assigned_to == request.user
            except Task.DoesNotExist:
                return False
        
        return True

    def has_object_permission(self, request, view, obj):
      return obj.task.owner == request.user or request.user in obj.task.assigned_to.all()

