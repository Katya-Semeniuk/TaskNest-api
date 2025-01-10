from rest_framework import permissions
from tasks.models import Task;

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAssignedOrOwner(permissions.BasePermission):
    """
    Custom permission to allow only task owners or assigned users to create comments.
    View-only access for authenticated users.
    """

    def has_permission(self, request, view):
        """
        Global permission check for the view.
        """
        # SAFE_METHODS (GET, HEAD, OPTIONS) - available only to logged in users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # POST method - we check if the user has the right to comment on the task
        if request.method == 'POST':
            task_id = request.data.get('task')  # ID of the task must be in request
            if not task_id:
                return False
            
            try:
                task = Task.objects.get(pk=task_id)
                return (
                    task.owner == request.user or
                    request.user in task.assigned_to.all()
                )
            except Task.DoesNotExist:
                return False

        return False

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission for update or delete.
        Only the owner of the comment can modify it.
        """
        return obj.owner == request.user


        

# class IsAssignedOrOwner(permissions.BasePermission):
#     """
#     Allows everyone to view comments, but only the assigned user
#     or owner of the task can create or modify a comment.
#     """

#     def has_permission(self, request, view):
#         # Дозволяємо читання для всіх
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Перевіряємо, чи користувач залогінений
#         if not request.user or not request.user.is_authenticated:
#             print(f"Access denied: user not authenticated. User: {request.user}")
#             return False

#         # Для створення коментарів (POST)
#         if request.method == 'POST':
#             task_id = request.data.get('task')  # Отримати ID завдання
#             print("Access denied: no task_id provided.")
#             if not task_id:
#                 return False
            
#             try:
#                 task = Task.objects.get(pk=task_id)
#                 # Дозволяємо тільки власнику або призначеному користувачу
#                 return task.owner == request.user or request.user in task.assigned_to.all()
#                 print(f"Task permissions check - Is owner: {is_owner}, Is assigned: {is_assigned}")
#             except Task.DoesNotExist:
#                 print(f"Access denied: task with id {task_id} does not exist.")
#                 return False

#         return True


#     def has_object_permission(self, request, view, obj):
#         is_owner = obj.task.owner == request.user
#         is_assigned = request.user in obj.task.assigned_to.all()
#         print(f"Object permissions check - Is owner: {is_owner}, Is assigned: {is_assigned}")
#         return is_owner or is_assigned


# class IsAssignedOrOwner(permissions.BasePermission):
#     """
#     Allows everyone to view comments, but only the assigned user
#     or owner of the task can create or modify a comment.
#     """
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         if view.action == 'create':
#             task_id = request.data.get('task')
#             if not task_id:
#                 return False
            
#             try:
#                 from tasks.models import Task 
#                 task = Task.objects.get(pk=task_id)
#                 return task.owner == request.user or task.assigned_to == request.user
#             except Task.DoesNotExist:
#                 return False
        
#         return True

#     def has_object_permission(self, request, view, obj):
#       return obj.task.owner == request.user or request.user in obj.task.assigned_to.all()

