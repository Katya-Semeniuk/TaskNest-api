from rest_framework import serializers
from .models import Profile
from tasks.serializers import TaskSerializer

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    tasks_count = serializers.ReadOnlyField()
    tasks = TaskSerializer(many=True, read_only=True, source='owner.tasks') 
   
    

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'image', 'is_owner', 'tasks_count', 'tasks'
        ]