from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    assigned_to = serializers.StringRelatedField(allow_null=True)
    is_overdue = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request.user != instance.owner:
            raise serializers.ValidationError("Only the owner can assign users")
        return super().update(instance, validated_data)


    class Meta:
        model = Task
        fields = [
            'id', 'owner','profile_id', 'title', 'description', 'due_date', 'created_at', 
            'updated_at', 'is_overdue', 'priority', 'category', 
            'status', 'assigned_to', 'is_owner',
        ]
