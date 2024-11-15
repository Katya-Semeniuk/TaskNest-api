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
        # Дозволяємо доступ до перегляду списку або деталей
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Для інших дій (наприклад, створення) потрібен об'єкт
        if view.action == 'create':
            # Перевіряємо, чи є користувач власником завдання або призначеним
            task_id = request.data.get('task')
            if not task_id:
                return False
            
            try:
                from tasks.models import Task  # Уникаємо циклічних імпортів
                task = Task.objects.get(pk=task_id)
                return task.owner == request.user or task.assigned_to == request.user
            except Task.DoesNotExist:
                return False
        
        return True

    def has_object_permission(self, request, view, obj):
        # Перевіряємо доступ до об'єкта коментаря
        is_task_owner_or_assigned = obj.task.owner == request.user or obj.task.assigned_to == request.user
        is_comment_owner = obj.owner == request.user
        return is_comment_owner or is_task_owner_or_assigned
