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
        # print(response.data)
        # print(len(response.data))

    def test_logged_in_user_can_create_task(self):
        self.client.login(username='testuser1', password='pass')
        response = self.client.post('/tasks/', {'title': 'a title'})
        count = Task.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_task(self):
        response = self.client.post('/tasks/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_update_task(self):
        self.client.login(username='testuser1', password='pass')
        testuser1 = User.objects.get(username='testuser1')
        task = Task.objects.create(owner=testuser1, title='a title')
        response = self.client.put(f'/tasks/{task.id}/', {'title': 'updated title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'updated title')

    def test_owner_can_delete_task(self):
        self.client.login(username='testuser1', password='pass')
        testuser1 = User.objects.get(username='testuser1')
        task = Task.objects.create(owner=testuser1, title='a title')
        response = self.client.delete(f'/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())


class PostDetailViewTests(APITestCase):
    def setUp(self):
        testuser1 = User.objects.create_user(username='testuser1', password='pass')
        testuser2 = User.objects.create_user(username='testuser2', password='pass')
        Task.objects.create(
            owner=testuser1, title='a title', description='testuser1 s description'
        )
        Task.objects.create(
            owner=testuser2, title='another title', description='testuser2 s description'
        )
    def test_can_retrieve_task_using_valid_id(self):
        response = self.client.get('/tasks/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_task_using_invalid_id(self):
        response = self.client.get('/tasks/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    

