from django.contrib.auth.models import User
from .models import Task
from rest_framework import status
from rest_framework.test import APITestCase

class TaskListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='testuser1', password='pass')

    def test_can_list_tasks(self):
        testuser1 = User.objects.get(username='testuser1')
        Task.objects.create(owner=testuser1, title='a title')
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))
