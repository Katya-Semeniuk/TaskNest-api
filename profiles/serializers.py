from rest_framework import serializers
from .models import Profile
from tasks.serializers import TaskSerializer
from tasks.models import Task 

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    tasks_count = serializers.ReadOnlyField()
    tasks = TaskSerializer(many=True, read_only=True, source='owner.tasks') 
    assigned_to_tasks = serializers.SerializerMethodField()
   
    

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_assigned_to_tasks(self, obj):
        tasks = Task.objects.filter(assigned_to=obj.owner)
        return TaskSerializer(tasks, many=True).data 

    

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'image', 'is_owner', 'tasks_count', 'tasks', 'assigned_to_tasks'
        ]