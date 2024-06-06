from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from todos.serializer import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from todos.models import Todo
# Create your views here.


class CreateTodoAPIView(CreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    

class TodoListAPIView( ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
    
 