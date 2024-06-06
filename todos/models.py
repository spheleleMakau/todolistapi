from django.db import models
from helpers.models import TrackingModel
from authentication.models import User
# Create your models here.

class Todo(TrackingModel):
    title = models.CharField(max_length=225)
    desc = models.TextField()
    is_complete = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    
    # ordering = ['title']
    # print(ordering)
    
    def __str__(self):
        return self.title