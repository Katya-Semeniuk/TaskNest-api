
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from drf_api.permissions import IsAssignedOrOwner, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class CommentList(generics.ListCreateAPIView):
    """
    List comments or create a comment if logged in and siggned in to the task.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAssignedOrOwner]

    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['task']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a comment, update or delete it by id if you own it.
    """
    permission_classes = [IsAssignedOrOwner]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()



