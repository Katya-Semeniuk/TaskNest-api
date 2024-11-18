from rest_framework import generics, permissions, status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class TaskList(generics.ListCreateAPIView):
    """
    List tasks or create a task if logged in
    The perform_create method associates the post with the logged in user
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Task.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a task if you're the owner.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Task.objects.all()

class AssignUserToTaskView(generics.UpdateAPIView):
    """
    Assign a user to a task (POST method).
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=user_id)

        if task.owner != request.user:
            return Response(
                {"error": "Only the owner can assign users to this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

        task.assigned_to.add(user)
        task.save()
        return Response({"message": f"User {user.username} assigned to the task."}, status=status.HTTP_200_OK)


class UnassignUserFromTaskView(generics.UpdateAPIView):
    """
    Unassign a user from a task (DELETE method).
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=user_id)

        if task.owner != request.user:
            return Response(
                {"error": "Only the owner can remove users from this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

        task.assigned_to.remove(user)
        task.save()
        return Response({"message": f"User {user.username} removed from the task."}, status=status.HTTP_200_OK)
