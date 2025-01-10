from django.db.models import Count
from rest_framework import generics, filters
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter



class ProfileList(generics.ListAPIView):
    """
    List all profiles
    No Create view (post method), as profile creation handled by django signals
    """

    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        tasks_count = Count('owner__task', distinct=True),
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        SearchFilter, 
    ]

    ordering_fields = [
        'tasks_count',
    ]

    search_fields = ['owner__username'] 



class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        tasks_count = Count('owner__tasks', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer