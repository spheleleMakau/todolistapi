# from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from todos.models import Todo
# Create your tests here.

class TodosAPITestCase(APITestCase):
    def create_todo(self):
        sample_todo = {'title': 'read a book', 'desc': 'we need to upskill daily'}
        response = self.client.post(reverse('todos'),sample_todo)
        
        return response
        
    def authenticate(self):
        self.client.post(reverse("register"),{
            'username' : 'sphelele' , 'email': 'makausg@gmail.com',
            'password': 'admin1234.'})
        
        response = self.client.post(reverse('login'),{'email': 'makausg@gmail.com',
            'password': 'admin1234.'})
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")
        print(response.data['token'])


class TestListCreateTodos(TodosAPITestCase):
        
    def test_should_not_create_todo_with_no_auth(self):
        response = self.create_todo()
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
    def test_should_create_todo(self):
        previous_todo_count = Todo.objects.all().count()
        self.authenticate()
        response = self.create_todo()
        self.assertEqual(Todo.objects.all().count(), previous_todo_count+1)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'],'read a book')
        self.assertEqual(response.data['desc'],'we need to upskill daily')
        
        
    def test_retrieve_all_todo(self):
        self.authenticate()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'],list)
        
        
# _____________    TESTING DETAILS APIVIEWS________________________________


class TestTodoDetailsAPIView(TodosAPITestCase):
    def test_retieves_one_item(self):
        self.authenticate()
        response = self.create_todo()
        
        
        res = self.client.get(reverse("todo",kwargs={'id': response.data['id']}))
        self.assertEqual(res.status_code,status.HTTP_200_OK)

        todo = Todo.objects.get(id=response.data['id'])
        self.assertEqual(todo.title, res.data['title'])
    
    def test_updates_one_item(self):
        self.authenticate()
        response = self.create_todo()
        res = self.client.patch(reverse("todo",kwargs={'id': response.data['id']}),{'title':'new one'})
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        
        updataed_todo = Todo.objects.get(id=response.data['id'])
        self.assertEqual(updataed_todo.title,'new one')        
    
    
    def test_delete_one_item(self):
        self.authenticate()
        response = self.create_todo()
        prev_db_count = Todo.objects.all().count()
        self.assertGreater(prev_db_count,0)
        
        res = self.client.delete(
            reverse("todo",kwargs={'id': response.data['id']}))
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)
        
        
        
    
        