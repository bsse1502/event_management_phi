from django.db import models

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Event Model
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    time = models.TimeField(auto_now=True)
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.name

# Participant Model
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    events = models.ManyToManyField(Event)  # No on_delete here

    def __str__(self):
        return self.name
