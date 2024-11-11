from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    assigned_to = serializers.ReadOnlyField(source='assigned_to.username')
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = [
            'id', 'owner','title', 'description', 'due_date', 'created_at', 
            'updated_at', 'is_overdue', 'priority', 'category', 
            'status', 'assigned_to', 'is_owner',
        ]
