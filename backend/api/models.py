from django.db import models
from django.contrib.auth.models import User

class SharedFiles(models.Model):
    file = models.ForeignKey("File", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class File(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(upload_to="uploads/")
    encrypted_symmetric_key = models.BinaryField(editable=False)
    iv = models.BinaryField(editable=False)
    shared_with = models.ManyToManyField(
        User, related_name="shared_files", blank=True
    )
    
    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        self.file.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
