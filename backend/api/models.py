from django.db import models
from django.contrib.auth.models import User

class SharedFiles(models.Model):
    file = models.ForeignKey('File', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class File(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to='uploads/')
    shared_with = models.ManyToManyField(User, related_name='shared_files', null=True, blank=True)

    def __str__(self):
        return self.title