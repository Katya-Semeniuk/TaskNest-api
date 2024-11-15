from rest_framework import viewsets
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsAssignedOrOwner
from rest_framework.permissions import IsAuthenticated

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAssignedOrOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



