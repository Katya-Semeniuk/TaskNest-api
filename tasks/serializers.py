from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    is_overdue = serializers.ReadOnlyField()
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())
    assigned_users = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()

    def get_assigned_users(self, obj):
        return [{"id": user.id, "username": user.username} for user in obj.assigned_to.all()]


    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request.user != instance.owner:
            raise serializers.ValidationError("Only the owner can assign users")
        return super().update(instance, validated_data)

    def get_serializer_context(self):
        return {'request': self.request}


    class Meta:
        model = Task
        fields = [
            'id', 'owner','profile_id', 'is_owner', 'title', 'description', 'due_date', 'created_at', 
            'updated_at', 'is_overdue', 'priority', 'category', 
            'status','assigned_to','assigned_users', 'comments_count',
        ]
