from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    assigned_to = serializers.ReadOnlyField(source='assigned_to.username')
    is_overdue = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Task
        fields = [
            'id', 'owner','profile_id', 'title', 'description', 'due_date', 'created_at', 
            'updated_at', 'is_overdue', 'priority', 'category', 
            'status', 'assigned_to', 'is_owner',
        ]
