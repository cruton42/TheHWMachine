from django.db import models

class Job(models.Model):
    url = models.URLField()
    header = models.CharField(max_length=255)
    description = models.TextField()  # Use TextField for longer text like job descriptions

    def __str__(self):
        return self.header
    
class twJob(models.Model):
    url = models.URLField()
    header = models.CharField(max_length=255)
    description = models.TextField()  # Use TextField for longer text like job descriptions

    def __str__(self):
        return self.header
